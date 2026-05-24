# Benchmark Result 63 from Run c98a68bc-fbb9-4771-ad89-f1bd1667c9e5

| Key            | Value                                |
|:---------------|:-------------------------------------|
| Benchmark UUID | c98a68bc-fbb9-4771-ad89-f1bd1667c9e5 |
| Run index      | 63                                   |
| Run UUID       | 35320776-a6a0-4324-bd31-b02b1cb05a06 |
| Scenario       | AI Reconnaissance                    |
| Setup          | eval_containerlab_bfh                |
| Timestamp      | 2026-05-24T02:02:09.065991+02:00     |
| Success        | No                                   |
| Duration (s)   | 2                                    |

--------------------------------------

Traceback (most recent call last):
  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/nsak/core/benchmark/benchmark_run.py", line 59, in execute
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

  File "/nsak/lib/scenarios/ai_reconnaissance/scenario.py", line 52, in run_reconnaissance_agent
    result = await agent.ainvoke(prompt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/nsak/core/ai/ai_agent.py", line 256, in ainvoke
    return await self.agent.ainvoke(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
        {"messages": [{"role": role, "content": prompt}]}, reasoning=True
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/pregel/main.py", line 4057, in ainvoke
    async for chunk in self.astream(
    ...<30 lines>...
            chunks.append(chunk)

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/pregel/main.py", line 3407, in astream
    async for _ in runner.atick(
    ...<16 lines>...
            yield o

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/pregel/_runner.py", line 396, in atick
    await arun_with_retry(
    ...<15 lines>...
    )

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/pregel/_retry.py", line 706, in arun_with_retry
    return await task.proc.ainvoke(task.input, config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/_internal/_runnable.py", line 733, in ainvoke
    input = await asyncio.create_task(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^
        step.ainvoke(input, config, **kwargs), context=context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/_internal/_runnable.py", line 501, in ainvoke
    ret = await self.afunc(*args, **kwargs)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain/agents/factory.py", line 1380, in amodel_node
    model_response = await _execute_model_async(request)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain/agents/factory.py", line 1352, in _execute_model_async
    output = await model_.ainvoke(messages)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/runnables/base.py", line 5894, in ainvoke
    return await self.bound.ainvoke(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/language_models/chat_models.py", line 497, in ainvoke
    llm_result = await self.agenerate_prompt(
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<8 lines>...
    )
    ^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/language_models/chat_models.py", line 1834, in agenerate_prompt
    return await self.agenerate(
           ^^^^^^^^^^^^^^^^^^^^^
        prompt_messages, stop=stop, callbacks=callbacks, **kwargs
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/language_models/chat_models.py", line 1792, in agenerate
    raise exceptions[0]

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/language_models/chat_models.py", line 2127, in _agenerate_with_cache
    result = await self._agenerate(
             ^^^^^^^^^^^^^^^^^^^^^^
        messages, stop=stop, run_manager=run_manager, **kwargs
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_openai/chat_models/base.py", line 1937, in _agenerate
    _handle_openai_api_error(e)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_openai/chat_models/base.py", line 1930, in _agenerate
    raw_response = await self.async_client.with_raw_response.create(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        **payload
        ^^^^^^^^^
    )
    ^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/openai/_legacy_response.py", line 384, in wrapped
    return cast(LegacyAPIResponse[R], await func(*args, **kwargs))
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/openai/resources/chat/completions/completions.py", line 2739, in create
    return await self._post(
           ^^^^^^^^^^^^^^^^^
    ...<53 lines>...
    )
    ^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/openai/_base_client.py", line 1931, in post
    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/openai/_base_client.py", line 1716, in request
    raise self._make_status_error_from_response(err.response) from None

InternalServerError: <html>
<head><title>502 Bad Gateway</title></head>
<body>
<center><h1>502 Bad Gateway</h1></center>
<hr><center>nginx/1.24.0 (Ubuntu)</center>
</body>
</html>
