"""Direct logical and unique-storage accounting for representative algorithm state."""
import argparse, csv, os, resource, time
from collections import defaultdict
import torch
from algorithm.dirbridge import build_count_sketch_plan


def tensor_records(obj, path='state', persistent=True, algorithm=True, seen=None):
    seen = {} if seen is None else seen
    out=[]
    if torch.is_tensor(obj):
        ptr=obj.untyped_storage().data_ptr() if obj.numel() else id(obj)
        storage_bytes=obj.untyped_storage().nbytes() if obj.numel() else 0
        rec={'path':path,'shape':str(tuple(obj.shape)),'dtype':str(obj.dtype),'device':str(obj.device),
             'logical_bytes':obj.numel()*obj.element_size(),'storage_ptr':str(ptr),'storage_offset':obj.storage_offset(),
             'unique_physical_bytes':storage_bytes if ptr not in seen else 0,'alias_of':seen.get(ptr,''),
             'persistent':persistent,'algorithm_state':algorithm}
        if ptr not in seen: seen[ptr]=path
        out.append(rec); return out
    if isinstance(obj, dict):
        for k,v in obj.items(): out += tensor_records(v, f'{path}.{k}', persistent, algorithm, seen)
    elif isinstance(obj, (list,tuple)):
        for i,v in enumerate(obj): out += tensor_records(v, f'{path}[{i}]', persistent, algorithm, seen)
    return out


def representative(method, P=10000, N=100, K0=7, ds=2048, device='cpu'):
    base={'weight':torch.zeros(P,dtype=torch.float32,device=device)}
    if method=='FedBuff': return {'fedbuff': {'last_aggregate':base}}
    if method=='CA2FL': return {'cache':[{'weight':torch.zeros(P,dtype=torch.float32,device=device)} for _ in range(N)], 'cache_mean':{'weight':torch.zeros(P,dtype=torch.float32,device=device)}}
    if method=='FADAS': return {'fadas_m':{'weight':torch.zeros(P,dtype=torch.float32,device=device)},'fadas_v':{'weight':torch.zeros(P,dtype=torch.float32,device=device)},'fadas_vhat':{'weight':torch.zeros(P,dtype=torch.float32,device=device)}}
    if method=='DirBridge':
        ref={'weight':torch.zeros(P,dtype=torch.float32,device=device)}
        plan=build_count_sketch_plan(ref,ds,17)
        buckets=[b.to(device) for _,b,_ in plan]; signs=[s.to(device) for _,_,s in plan]
        return {'group_cache':[{'weight':torch.zeros(P,dtype=torch.float32,device=device)} for _ in range(K0)], 'client_features':torch.zeros(N,ds,dtype=torch.float32,device=device), 'group_centroids':torch.zeros(K0,ds,dtype=torch.float32,device=device), 'group_ids':torch.zeros(N,dtype=torch.int64,device=device), 'group_counts':torch.zeros(K0,dtype=torch.int64,device=device), 'count_sketch_bucket':buckets, 'count_sketch_sign':signs}
    raise ValueError(method)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); ap.add_argument('--device',default='cpu'); args=ap.parse_args()
    rows=[]
    for method in ['FedBuff','CA2FL','DirBridge','FADAS']:
        state=representative(method,device=args.device); rec=tensor_records(state, path=f'{method}.algorithm_state')
        for r in rec: r['method']=method; rows.append(r)
    os.makedirs(os.path.dirname(args.out),exist_ok=True)
    with open(args.out,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['method','path','shape','dtype','device','logical_bytes','storage_ptr','storage_offset','unique_physical_bytes','alias_of','persistent','algorithm_state']); w.writeheader(); w.writerows(rows)
    print('rows',len(rows),'logical_bytes',sum(int(r['logical_bytes']) for r in rows),'unique_bytes',sum(int(r['unique_physical_bytes']) for r in rows))
    print('rss_kb',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

if __name__=='__main__': main()
