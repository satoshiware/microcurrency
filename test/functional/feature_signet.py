#!/usr/bin/env python3
# Copyright (c) 2019-2021 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test basic signet functionality"""

from decimal import Decimal

from test_framework.test_framework import MicrocurrencyTestFramework
from test_framework.util import assert_equal

signet_blocks = [
    '00000020f61eee3b63a380a477a063af32b2bbc97c9ff9f01f2c4225e973988108000000f575c83235984e7dc4afc1f30944c170462e84437ab6f2d52e16878a79e4678bd1914d5fae77031eccf4070001010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025151feffffff0200f2052a010000001600149243f727dd5343293eb83174324019ec16c2630f0000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402205e423a8754336ca99dbe16509b877ef1bf98d008836c725005b3c787c41ebe46022047246e4467ad7cc7f1ad98662afcaf14c115e0095a227c7b05c5182591c23e7e01000120000000000000000000000000000000000000000000000000000000000000000000000000',
    '00000020533b53ded9bff4adc94101d32400a144c54edc5ed492a3b26c63b2d686000000b38fef50592017cfafbcab88eb3d9cf50b2c801711cad8299495d26df5e54812e7914d5fae77031ecfdd0b0001010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025251feffffff0200f2052a01000000160014fd09839740f0e0b4fc6d5e2527e4022aa9b89dfa0000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa24900473044022031d64a1692cdad1fc0ced69838169fe19ae01be524d831b95fcf5ea4e6541c3c02204f9dea0801df8b4d0cd0857c62ab35c6c25cc47c930630dc7fe723531daa3e9b01000120000000000000000000000000000000000000000000000000000000000000000000000000',
    '000000202960f3752f0bfa8858a3e333294aedc7808025e868c9dc03e71d88bb320000007765fcd3d5b4966beb338bba2675dc2cf2ad28d4ad1d83bdb6f286e7e27ac1f807924d5fae77031e81d60b0001010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025351feffffff0200f2052a010000001600141e5fb426042692ae0e87c070e78c39307a5661c20000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402205de93694763a42954865bcf1540cb82958bc62d0ec4eee02070fb7937cd037f4022067f333753bce47b10bc25eb6e1f311482e994c862a7e0b2d41ab1c8679fd1b1101000120000000000000000000000000000000000000000000000000000000000000000000000000',
    '00000020b06443a13ae1d3d50faef5ecad38c6818194dc46abca3e972e2aacdae800000069a5829097e80fee00ac49a56ea9f82d741a6af84d32b3bc455cf31871e2a8ac27924d5fae77031e9c91050001010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025451feffffff0200f2052a0100000016001430db2f8225dcf7751361ab38735de08190318cb70000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402200936f5f9872f6df5dd242026ad52241a68423f7f682e79169a8d85a374eab9b802202cd2979c48b321b3453e65e8f92460db3fca93cbea8539b450c959f4fbe630c601000120000000000000000000000000000000000000000000000000000000000000000000000000',
    '000000207ed403758a4f228a1939418a155e2ebd4ae6b26e5ffd0ae433123f7694010000542e80b609c5bc58af5bdf492e26d4f60cd43a3966c2e063c50444c29b3757a636924d5fae77031ee8601d0001010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025551feffffff0200f2052a01000000160014edc207e014df34fa3885dff97d1129d356e1186a0000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa24900473044022021a3656609f85a66a2c5672ed9322c2158d57251040d2716ed202a1fe14f0c12022057d68bc6611f7a9424a7e00bbf3e27e6ae6b096f60bac624a094bc97a59aa1ff01000120000000000000000000000000000000000000000000000000000000000000000000000000',
    '000000205bea0a88d1422c3df08d766ad72df95084d0700e6f873b75dd4e986c7703000002b57516d33ed60c2bdd9f93d6d5614083324c837e68e5ba6e04287a7285633585924d5fae77031ed171960001010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025651feffffff0200f2052a010000001600143ae612599cf96f2442ce572633e0251116eaa52f0000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa24900473044022059a7c54de76bfdbb1dd44c78ea2dbd2bb4e97f4abad38965f41e76433e56423c022054bf17f04fe17415c0141f60eebd2b839200f574d8ad8d55a0917b92b0eb913401000120000000000000000000000000000000000000000000000000000000000000000000000000',
    '00000020daf3b60d374b19476461f97540498dcfa2eb7016238ec6b1d022f82fb60100007a7ae65b53cb988c2ec92d2384996713821d5645ffe61c9acea60da75cd5edfa1a944d5fae77031e9dbb050001010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025751feffffff0200f2052a01000000160014ef2dceae02e35f8137de76768ae3345d99ca68860000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402202b3f946d6447f9bf17d00f3696cede7ee70b785495e5498274ee682a493befd5022045fc0bcf9332243168b5d35507175f9f374a8eba2336873885d12aada67ea5f601000120000000000000000000000000000000000000000000000000000000000000000000000000',
    '00000020457cc5f3c2e1a5655bc20e20e48d33e1b7ea68786c614032b5c518f0b6000000541f36942d82c6e7248275ff15c8933487fbe1819c67a9ecc0f4b70bb7e6cf672a944d5fae77031e8f39860001010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025851feffffff0200f2052a0100000016001472a27906947c06d034b38ba2fa13c6391a4832790000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402202d62805ce60cbd60591f97f949b5ea5bd7e2307bcde343e6ea8394da92758e72022053a25370b0aa20da100189b7899a8f8675a0fdc60e38ece6b8a4f98edd94569e01000120000000000000000000000000000000000000000000000000000000000000000000000000',
    '00000020a2eb61eb4f3831baa3a3363e1b42db4462663f756f07423e81ed30322102000077224de7dea0f8d0ec22b1d2e2e255f0a987b96fe7200e1a2e6373f48a2f5b7894954d5fae77031e36867e0001010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025951feffffff0200f2052a01000000160014aa0ad9f26801258382e0734dceec03a4a75f60240000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402206fa0d59990eed369bd7375767c9a6c9369fae209152b8674e520da270605528c0220749eed3b12dbe3f583f505d21803e4aef59c8e24c5831951eafa4f15a8f92c4e01000120000000000000000000000000000000000000000000000000000000000000000000000000',
    '00000020a868e8514be5e46dabd6a122132f423f36a43b716a40c394e2a8d063e1010000f4c6c717e99d800c699c25a2006a75a0c5c09f432a936f385e6fce139cdbd1a5e9964d5fae77031e7d026e0001010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025a51feffffff0200f2052a01000000160014aaa671c82b138e3b8f510cd801e5f2bd0aa305940000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa24900473044022042309f4c3c7a1a2ac8c24f890f962df1c0086cec10be0868087cfc427520cb2702201dafee8911c269b7e786e242045bb57cef3f5b0f177010c6159abae42f646cc501000120000000000000000000000000000000000000000000000000000000000000000000000000',
]


class SignetBasicTest(MicrocurrencyTestFramework):
    def set_test_params(self):
        self.chain = "signet"
        self.num_nodes = 6
        self.setup_clean_chain = True
        shared_args1 = ["-signetchallenge=51"]  # OP_TRUE
        shared_args2 = []  # default challenge
        # we use the exact same challenge except we do it as a 2-of-2, which means it should fail
        shared_args3 = ["-signetchallenge=522103ad5e0edad18cb1f0fc0d28a3d4f1f3e445640337489abb10404f2d1e086be430210359ef5021964fe22d6f8e05b2463c9540ce96883fe3b278760f048f5189f2e6c452ae"]

        self.extra_args = [
            shared_args1, shared_args1,
            shared_args2, shared_args2,
            shared_args3, shared_args3,
        ]

    def run_test(self):
        self.log.info("basic tests using OP_TRUE challenge")

        self.log.info('getmininginfo')
        mining_info = self.nodes[0].getmininginfo()
        assert_equal(mining_info['blocks'], 0)
        assert_equal(mining_info['chain'], 'signet')
        assert 'currentblocktx' not in mining_info
        assert 'currentblockweight' not in mining_info
        assert_equal(mining_info['networkhashps'], Decimal('0'))
        assert_equal(mining_info['pooledtx'], 0)

        self.generate(self.nodes[0], 1, sync_fun=self.no_op)

        self.log.info("pregenerated signet blocks check")

        height = 0
        for block in signet_blocks:
            assert_equal(self.nodes[2].submitblock(block), None)
            height += 1
            assert_equal(self.nodes[2].getblockcount(), height)

        self.log.info("pregenerated signet blocks check (incompatible solution)")

        assert_equal(self.nodes[4].submitblock(signet_blocks[0]), 'bad-signet-blksig')

        self.log.info("test that signet logs the network magic on node start")
        with self.nodes[0].assert_debug_log(["Signet derived magic (message start)"]):
            self.restart_node(0)


if __name__ == '__main__':
    SignetBasicTest().main()
