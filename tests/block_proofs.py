import asyncio
import time

from tonpylib.liteclient.client_tcp import AdnlClientTcp
from tonpylib.tl.block import BlockIdExt

host = '65.21.141.231'
port = 17728

pub_key_b64 = 'BYSVpL7aPk0kU5CtlsIae/8mf2B/NrBi7DKmepcjX6Q='


async def main():
    client = AdnlClientTcp(
        host,
        port,
        pub_key_b64
    )
    await client.connect()

    await client.get_masterchain_info()
    last = BlockIdExt.from_dict((await client.get_masterchain_info_ext())['last'])

    blk, blk_data = await client.lookup_block(-1, -9223372036854775808, last.seqno - 100)
    await client.get_block_proof(known_block=last, target_block=blk)

    init_block = BlockIdExt.from_dict({
      "root_hash": "61192b72664cbcb06f8da9f0282c8bdf0e2871e18fb457e0c7cca6d502822bfe",
      "seqno": 27747086,
      "file_hash": "378db1ccf9c98c3944de1c4f5ce6fea4dcd7a26811b695f9019ccc3e7200e35b",
      "workchain": -1,
      "shard": -9223372036854775808
    })

    s = time.time()

    await client.get_block_proof(known_block=init_block, target_block=blk)
    print(time.time() - s)

    await client.close()


if __name__ == '__main__':
    asyncio.run(main(), debug=True)
