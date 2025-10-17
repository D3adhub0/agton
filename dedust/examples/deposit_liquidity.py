from os import getenv

from agton.ton import ToncenterClient, Address, to_nano, to_units
from agton.wallet import WalletV3R2
from agton.jetton import JettonMaster
from agton.dedust import Factory
from agton.dedust.types import PoolParams, Volatile
import agton.dedust.types.asset as Asset

usdt_address = Address.parse('EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs')

mnemonic = getenv('WALLET_MNEMONIC')
assert mnemonic is not None

provider = ToncenterClient(net='mainnet')
my_wallet = WalletV3R2.from_mnemonic(provider, mnemonic)
my_usdt_wallet = JettonMaster(provider, usdt_address).get_jetton_wallet(my_wallet.address)

usdt = Asset.Jetton(usdt_address)
ton = Asset.Native()

factory = Factory.from_mainnet(provider)

ton_usdt_pool = factory.get_pool(ton, usdt)
ton_vault = factory.get_vault(ton)
usdt_vault = factory.get_vault(usdt)

asset0_target_balance = to_nano(1)
asset1_target_balance = to_units(0.5, 6)

deposit_ton = ton_vault.create_deposit_liquidity_message(
    value=asset0_target_balance + to_nano(0.5),
    deposit_liquidity_body=ton_vault.create_deposit_liquidity_body(
        query_id=0,
        amount=asset0_target_balance,
        pool_params=PoolParams(Volatile(), ton, usdt),
        min_lp_amount=0,
        asset0_target_balance=asset0_target_balance,
        asset1_target_balance=asset1_target_balance,
    )
)

deposit_usdt = usdt_vault.create_deposit_liquidity_message(
    jetton_wallet=my_usdt_wallet,
    query_id=1,
    amount=asset1_target_balance,
    response_destination=my_wallet.address,
    deposit_liquidity_payload=usdt_vault.create_deposit_liquidity_payload(
        pool_params=PoolParams(Volatile(), ton, usdt),
        min_lp_amount=0,
        asset0_target_balance=asset0_target_balance,
        asset1_target_balance=asset1_target_balance,
    )
)


signed_external = my_wallet.create_signed_external(
    messages_with_modes=[(deposit_ton, 3), (deposit_usdt, 3)],
    valid_until=(1 << 32) - 1,
    seqno=my_wallet.seqno(),
    use_dummy_private_key=True,
)

# provider.send_external_message(signed_external)
print("https://tonviewer.com/emulate/" + signed_external.to_cell().to_boc().hex())
