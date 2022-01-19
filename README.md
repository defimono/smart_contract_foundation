# Algorand Smart Contract Foundation

[![Pull Request](https://github.com/defimono/smart_contract_foundation/actions/workflows/pull_request.yaml/badge.svg)](https://github.com/defimono/smart_contract_foundation/actions/workflows/pull_request.yaml)

![alt logo](./algorand_full_logo_black.png)

## Description

Foundational smart contracts and related PyTeal templates for DeFi Mono that comprise key areas of the platform and
supporting systems. These have been provided as a tool to improve the community, Algorand ecosystem, educate, etc. as
well as provide the key contracts for external public security access, access, and collaboration.

## Contracts

Currently, the testnet implementation is nearing completion for the following smart contract application groups.

### Reserve

The Reserve, or smart bank, is an application that allows users to stake funds, and get money out of the product
according to various business logic gates built in. This portion of the code is proprietary, but you may see the other
half that we connect to for business logic and audit.

The central reserve place that holds funds is a stateless smart signature contract account, allowing any deposit of
Algorand or USDC assets from anywhere, but limiting with logic how it pays out and can be withdrawn from. Currently,
there is one application only that is whitelisted for interaction with the smart signature itself.

### Contract Collection

Local state for smart contracts for each user is limited to 16 items of either Bytearray (Bytes) or Uint64. This is a
helper smart contract to be called in collaboration with others to tie callers to what contracts they have assigned to
themselves and track their state, and usage, of the application.
 
This allows the platform to not host dedicated database software to tie users to their current items for their account,
we end up using the blockchain natively for this function in subsequent atomic transaction groups. This elimantes also
the state desync failure that would potentially occur if an API or database become unavailable.

## Contributing

We are still working on general community guidelines for contributing, in the meantime please follow the process below
until we are able to define them

1. Fork the repo on GitHub
2. Clone the project to your own machine
3. Commit changes to your own branch
4. Push your work back up to your fork
5. Submit a Pull request so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!
