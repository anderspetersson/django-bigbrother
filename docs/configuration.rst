Configuration
=============

Bigbrother ships with a few modules. If you want to remove a or add a module, use the  `BIGBROTHER_MODULES` setting:

.. code-block:: python

    BIGBROTHER_MODULES = (
        # Default Modules:
        'bigbrother.core.UserCount',
        'bigbrother.core.NewUsersTodayCount',
        'bigbrother.core.FreeRamCount',
        'bigbrother.core.FreeDiskCount',

        # Modules not enabled by default:
        # 'bigbrother.core.SwapUsage',
    )