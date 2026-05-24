# Benchmark Result 17 from Run 01849539-65f9-415d-9b38-5f5bb07037bf

| Key            | Value                                |
|:---------------|:-------------------------------------|
| Benchmark UUID | 01849539-65f9-415d-9b38-5f5bb07037bf |
| Run index      | 17                                   |
| Run UUID       | 0401740c-9680-40e3-9fde-87eeedf2a9fe |
| Scenario       | AI Reconnaissance                    |
| Setup          | evaluation-containerlab-local        |
| Timestamp      | 2026-05-24T15:15:56.560542+02:00     |
| Success        | No                                   |
| Duration (s)   | 203                                  |

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
