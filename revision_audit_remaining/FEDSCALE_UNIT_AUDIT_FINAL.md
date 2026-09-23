# FedScale physical unit audit

The inspected production path is `utils/fedscale_trace.py::_profile_duration`, which computes `3 * batch * local_steps * computation / 1000 + (upload + download) / communication`. `test_fedscale_unit_chain.py` calls that production function directly and passes for a bounded synthetic profile.

The requested official FedScale payload chain could not be completed: the desktop checkout did not expose `fedscale/cloud/client_manager.py` or `client_metadata.py`, and browser-use public-source verification failed because the browser daemon connection was permission-blocked. The suspected `sys.getsizeof(pickle.dumps(model))*8/1024` caller therefore remains unverified. The local implementation's numeric factor is documented, but this is not evidence that the historical E4 payload used the same physical units. No official-chain equivalence claim is made.
