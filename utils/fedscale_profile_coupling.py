"""Profile-only KMeans coupling between label groups and FedScale profiles."""
import math
import pickle
from collections import defaultdict
import numpy as np


def _kmeans(x, k, seed, iterations=100):
    rng=np.random.default_rng(seed); centers=x[rng.choice(len(x), k, replace=False)].copy()
    for _ in range(iterations):
        d=((x[:,None,:]-centers[None,:,:])**2).sum(2); a=d.argmin(1)
        new=np.array([x[a==j].mean(0) if np.any(a==j) else centers[j] for j in range(k)])
        if np.allclose(new,centers): break
        centers=new
    return a,centers


def build_profile_coupling(profile_path, label_group_ids, batch_size, local_steps, upload_size=1.0, download_size=None, seed=0, num_groups=3):
    if download_size is None: download_size = upload_size
    with open(profile_path,'rb') as f: payload=pickle.load(f)
    rows=[]
    for pid, rec in payload.items():
        c=float(rec['computation']); b=float(rec['communication'])
        if c>0 and b>0 and math.isfinite(c) and math.isfinite(b): rows.append((str(pid),c,b))
    x=np.array([[math.log(c),math.log(b)] for _,c,b in rows],dtype=float)
    mu=x.mean(0); sd=x.std(0); z=(x-mu)/np.where(sd>0,sd,1)
    cls,centers=_kmeans(z,num_groups,seed)
    def duration(i):
        _,c,b=rows[i]; return 3.0*batch_size*local_steps*c/1000.0+(upload_size+download_size)/b
    order=sorted(range(num_groups),key=lambda j: float(np.median([duration(i) for i in range(len(rows)) if cls[i]==j])))
    rank={j:r for r,j in enumerate(order)}
    rng=np.random.default_rng(seed+104729); perm=rng.permutation(num_groups)
    label_to_class={g:int(perm[g]) for g in range(num_groups)}
    by=defaultdict(list)
    for i,j in enumerate(cls): by[int(j)].append(i)
    by = {j: sorted(indices, key=duration) for j, indices in by.items()}
    mapping=[]; reuse=0
    for client,g in enumerate(label_group_ids):
        cand=by[label_to_class[int(g)]]
        pos=sum(1 for old in mapping if old["label_group"]==int(g))
        i=cand[pos%len(cand)]; reuse += pos>=len(cand)
        mapping.append({"client_index":client,"label_group":int(g),"profile_id":rows[i][0],"profile_class":label_to_class[int(g)],"duration":duration(i),"cycled":bool(pos>=len(cand))})
    return {"mapping": mapping, "profile_cluster_sizes": {str(j): int((cls == j).sum()) for j in range(num_groups)}, "profile_cluster_order_fast_to_slow": [int(j) for j in order], "label_to_profile_class": label_to_class, "profile_reuse_count": int(reuse), "features": ["log_computation", "log_communication"], "kmeans": "custom_lloyd"}
