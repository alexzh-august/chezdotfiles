
Chain Testing Checklist
=======================

This checklist tracks the validation of daily volumes collection for all supported chains.
Date range for all testing: **2025-12-01 to 2025-12-31**.

Complete Chain Checklist
------------------------

All chains from ``CONFIG_BY_CHAIN`` with their chain IDs and native tickers:

**EVM Chains:**

phase 1
Chain.SONIC: VolumeConfig.from_chain(Chain.SONIC, "sonicusd"),
Chain.PLASMA: VolumeConfig.from_chain(Chain.PLASMA, "ethusd"),
Chain.INK: VolumeConfig.from_chain(Chain.INK, "ethusd"),
Chain.MONAD: VolumeConfig.from_chain(Chain.MONAD, "ethusd"),
Chain.POLYGON: VolumeConfig.from_chain(Chain.POLYGON, "maticusd"),
Chain.UNICHAIN: VolumeConfig.from_chain(Chain.UNICHAIN, "ethusd"),
phase 2 (re-validation of phase 1 chains with different date ranges)
# Note: These chains are intentionally repeated for validation across phases
Chain.MONAD: VolumeConfig.from_chain(Chain.MONAD, "ethusd"),
Chain.POLYGON: VolumeConfig.from_chain(Chain.POLYGON, "maticusd"),
Chain.UNICHAIN: VolumeConfig.from_chain(Chain.UNICHAIN, "ethusd"),
phase 3 
Chain.ARBITRUM: VolumeConfig.from_chain(Chain.ARBITRUM, "ethusd"),
Chain.BASE: VolumeConfig.from_chain(Chain.BASE, "ethusd"),
Chain.AVALANCHE: VolumeConfig.from_chain(Chain.AVALANCHE, "avaxusd"),
Chain.BSC: VolumeConfig.from_chain(Chain.BSC, "bnbusd"),
Chain.SCROLL: VolumeConfig.from_chain(Chain.SCROLL, "ethusd"),
Chain.LINEA: VolumeConfig.from_chain(Chain.LINEA, "ethusd"),
Chain.OPTIMISM: VolumeConfig.from_chain(Chain.OPTIMISM, "ethusd"),
Chain.BERA: VolumeConfig.from_chain(Chain.BERA, "berausd"),
Chain.HYPEREVM: VolumeConfig.from_chain(Chain.HYPEREVM, "hyperusdt"),

---------------------------------------------------------