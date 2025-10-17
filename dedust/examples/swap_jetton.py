from os import getenv

from agton.ton import ToncenterClient, Address, to_units
from agton.wallet import WalletV3R2
from agton.jetton import JettonMaster
from agton.dedust import Factory
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

swap_message = usdt_vault.create_swap_message(
    jetton_wallet=my_usdt_wallet,
    query_id=0,
    amount=to_units(0.5, 6),
    response_destination=my_wallet.address,
    swap_payload=usdt_vault.create_swap_payload(
        swap_step=ton_usdt_pool.pack_swap_step(limit=0),
        swap_params=usdt_vault.create_swap_params(
            recepient_addr=my_wallet.address,
        )
    )
)

signed_external = my_wallet.create_signed_external(
    messages_with_modes=[(swap_message, 3)],
    valid_until=(1 << 32) - 1,
    seqno=my_wallet.seqno(),
    use_dummy_private_key=True,
)

# provider.send_external_message(signed_external)
print("https://tonviewer.com/emulate/" + signed_external.to_cell().to_boc().hex())
