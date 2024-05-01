// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.19 <0.9.0;

import { ERC20Permit } from "./ERC20Permit.sol";
import { ERC20 } from "./ERC20.sol";

abstract contract IERC20Permit is ERC20Permit {
    function mint() external virtual;
}
