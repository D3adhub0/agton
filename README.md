# agton

**Python 3.12+ TON Blockchain SDK** intended for low level interacting with TON primitives but also giving ability to write high level contract wrappers

It is a package with namespace, currently there are following packages
- `agton` with core features
- `agton-wallet` with wallets wrapper (currently only V3R2 is implemeted)
- `agton-jetton` with jetton wrappers TEP-74
- `agton-dedust` with DeDust SDK (currently incomplete)

## Installation
Only core features
```bash
pip install agton
```
Or with selected optional dependencies
```bash
pip install agton[wallet,jetton]
```
Or with all optional dependencies
```bash
pip install agton[all]
```

## Tour
Please see [tour over core functionality](ton/README.md)

## Optional packages examples
- `agton-wallet` [example](wallet/README.md)
- `agton-jetton` [example](jetton/README.md)
- `agton-dedust` [example](dedust/README.md)
