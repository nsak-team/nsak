# Benchmark Result 2 from Run 5e556940-04a1-4e3e-a7a5-526cb1f3f9c1

| Key            | Value                                |
|:---------------|:-------------------------------------|
| Benchmark UUID | 5e556940-04a1-4e3e-a7a5-526cb1f3f9c1 |
| Run index      | 2                                    |
| Run UUID       | 5a613c94-b018-4941-a841-cb8c8fb98cf5 |
| Scenario       | AI Reconnaissance                    |
| Setup          | evaluation-containerlab-frontier     |
| Timestamp      | 2026-05-22T16:03:48.835463+02:00     |
| Success        | No                                   |
| Duration (s)   | 0                                    |

--------------------------------------

Traceback (most recent call last):
  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/nsak/core/benchmark/benchmark_run.py", line 56, in execute
    scenario_result = ScenarioManager.execute(
        self.scenario, **self.scenario_kwargs
    )

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/nsak/core/scenario/scenario_manager.py", line 345, in execute
    result = asyncio.run(run_fn(**arguments))

  File "/usr/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^

  File "/usr/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^

  File "/usr/lib/python3.13/asyncio/base_events.py", line 725, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^

  File "/nsak/lib/scenarios/ai_reconnaissance/scenario.py", line 111, in run
    raise ValueError("config.ai must be configured!")

ValueError: config.ai must be configured!
