# Benchmark Result 4 from Run 8e5fbd3a-4c89-4fc9-983f-a2fbaef5fd96

| Key            | Value                                |
|:---------------|:-------------------------------------|
| Benchmark UUID | 8e5fbd3a-4c89-4fc9-983f-a2fbaef5fd96 |
| Run index      | 4                                    |
| Run UUID       | 563fb7fa-ea2c-4a65-a712-b4c13496b059 |
| Scenario       | AI Reconnaissance                    |
| Setup          | eval_containerlab_bfh                |
| Timestamp      | 2026-05-24T17:13:14.935072+02:00     |
| Success        | No                                   |
| Duration (s)   | 445                                  |

--------------------------------------

Traceback (most recent call last):
  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/nsak/core/benchmark/benchmark_run.py", line 61, in execute
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

  File "/nsak/lib/scenarios/ai_reconnaissance/scenario.py", line 90, in run
    result, agent = await run_reconnaissance_agent(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
    )
    ^

  File "/nsak/lib/scenarios/ai_reconnaissance/scenario.py", line 75, in run_reconnaissance_agent
    raise ValueError("Could get structured output from response!")

ValueError: Could get structured output from response!
