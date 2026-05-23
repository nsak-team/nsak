# Benchmark Result 1 from Run 473b81bf-b3d1-45f1-b314-bcb7938db963

| Key            | Value                                |
|:---------------|:-------------------------------------|
| Benchmark UUID | 473b81bf-b3d1-45f1-b314-bcb7938db963 |
| Run index      | 1                                    |
| Run UUID       | 93d0e922-52e2-4c3d-81f9-c2c39f4b5790 |
| Scenario       | AI Reconnaissance                    |
| Setup          | evaluation-containerlab-local        |
| Timestamp      | 2026-05-22T17:52:01.737111+02:00     |
| Success        | No                                   |
| Duration (s)   | 384                                  |

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

  File "/nsak/lib/scenarios/ai_reconnaissance/scenario.py", line 113, in run
    result, agent = await run_reconnaissance_agent(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
    )
    ^

  File "/nsak/lib/scenarios/ai_reconnaissance/scenario.py", line 98, in run_reconnaissance_agent
    raise ValueError("Could get structured output from response!")

ValueError: Could get structured output from response!
