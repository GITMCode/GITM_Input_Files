# Running the Gannon Storm

- The IMF file listed here contains data merged from OMNIWeb and [this repository](https://github.com/spacecataz/swmf_runfiles/tree/main/May2024),
opting for the second when possible.
- AE data is downloaded from SuperMag, using the [GITM supermag_download_ae.py](https://github.com/GITMCode/GITM/blob/main/srcPython/supermag_download_ae.py) script.


Additionally, some changes to GITM were necessary to get GITM to finish running the Gannon storm.

---

## GITM Changes

- Expand lower latitude limit of Weimer. Weimer patterns for this storm extend past 45deg magnetic latitude. We need to expand the auroral oval
  - Change the 45 -> 10 on [line 422 of EIE_UaLibrary.f90](https://github.com/GITMCode/GITM/blob/2ba06740be25777cff47d519ced102a3fadc6561/util/EMPIRICAL/srcIE/EIE_UaLibrary.f90#L422)
  - This will become outdated as soon as the next "official" "release" of GITM is made.
- Additional limits to the solar wind values *may* be necessary, depending on the IMF file used.
  - See [this discussion](https://github.com/GITMCode/GITM/pull/32#issuecomment-2468371463) for more information
- Only advect O+, not NO+ & O+.
  - Change nIonsAdvect from 2 to 1 on [line 39 of ModEarth.f90](https://github.com/abukowski21/GITM/blob/6cd52cf068dcb2ac2f88af6b33a95d69eb0e8d8d/src/ModEarth.f90#L39)
- Do not crash when encountering negative ion densities.
  - Rather, when ion densities at the upper boundary get too low, enforce a different boundary condition to nudge the simulation back into reality & oprint a message that this happened.
  - The above fixes will likely make this unnecessary. I am including it for completeness though.
  - Comment out [line 637 of set_vertical_bcs.Earth.f90](https://github.com/GITMCode/GITM/blob/2ba06740be25777cff47d519ced102a3fadc6561/src/set_vertical_bcs.Earth.f90#L637), which makes the call to `stop_gitm`

Most of these changes will require GITM to be recompiled. Best practice would be to clean too, not just `make`:

```bash
make clean && make
```

Good luck!
