# Benchmark Result 3 from Run 4495e9b1-9c55-4049-8c01-3bb1f1b49e0e

| Key            | Value                                |
|:---------------|:-------------------------------------|
| Benchmark UUID | 4495e9b1-9c55-4049-8c01-3bb1f1b49e0e |
| Run index      | 3                                    |
| Run UUID       | a00d3399-c5ef-4ece-9adb-5fbcae506ca7 |
| Scenario       | AI Reconnaissance Multi Agent        |
| Setup          | eval_containerlab_bfh_multi_agent    |
| Timestamp      | 2026-05-24T21:40:39.552090+02:00     |
| Success        | No                                   |
| Duration (s)   | 2327                                 |

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

  File "/nsak/lib/scenarios/ai_reconnaissance_multi_agent/scenario.py", line 162, in run
    enumerate_services_result, enumerate_services_agent = await enumerate_services(
                                                          ^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
    )
    ^

  File "/nsak/lib/scenarios/ai_reconnaissance_multi_agent/scenario.py", line 103, in enumerate_services
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

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/prebuilt/tool_node.py", line 858, in _afunc
    outputs = await asyncio.gather(*coros)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/prebuilt/tool_node.py", line 1216, in _arun_one
    content = _handle_tool_error(e, flag=self._handle_tool_errors)

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/prebuilt/tool_node.py", line 434, in _handle_tool_error
    content = flag(e)  # type: ignore [assignment, call-arg]

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/prebuilt/tool_node.py", line 391, in _default_handle_tool_errors
    raise e

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/prebuilt/tool_node.py", line 1207, in _arun_one
    return await self._awrap_tool_call(tool_request, execute)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/nsak/core/ai/ai_agent.py", line 60, in awrap_tool_call
    return await handler(request)
           ^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/prebuilt/tool_node.py", line 1198, in execute
    return await self._execute_tool_async(req, input_type, config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/prebuilt/tool_node.py", line 1153, in _execute_tool_async
    content = _handle_tool_error(e, flag=self._handle_tool_errors)

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/prebuilt/tool_node.py", line 434, in _handle_tool_error
    content = flag(e)  # type: ignore [assignment, call-arg]

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/prebuilt/tool_node.py", line 391, in _default_handle_tool_errors
    raise e

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langgraph/prebuilt/tool_node.py", line 1105, in _execute_tool_async
    response = await tool.ainvoke(call_args, config)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/tools/structured.py", line 68, in ainvoke
    return await run_in_executor(config, self.invoke, input, config, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/runnables/config.py", line 667, in run_in_executor
    return await asyncio.get_running_loop().run_in_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
    )
    ^

  File "/usr/lib/python3.13/concurrent/futures/thread.py", line 59, in run
    result = self.fn(*self.args, **self.kwargs)

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/runnables/config.py", line 658, in wrapper
    return func(*args, **kwargs)

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/tools/base.py", line 642, in invoke
    return self.run(tool_input, **kwargs)
           ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/tools/base.py", line 1001, in run
    raise error_to_raise

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/tools/base.py", line 967, in run
    response = context.run(self._run, *tool_args, **tool_kwargs)

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/langchain_core/tools/structured.py", line 97, in _run
    return self.func(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/nsak/core/ai/tools/send_email.py", line 50, in send_email
    email_backend.send(subject, content, cc_recipients, attachments)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/root/.local/share/uv/tools/nsak/lib/python3.13/site-packages/nsak/core/email/email_backend.py", line 111, in send
    self.backend.send_message(email)
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^

  File "/usr/lib/python3.13/smtplib.py", line 989, in send_message
    return self.sendmail(from_addr, to_addrs, flatmsg, mail_options,
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                         rcpt_options)
                         ^^^^^^^^^^^^^

  File "/usr/lib/python3.13/smtplib.py", line 884, in sendmail
    (code, resp) = self.mail(from_addr, esmtp_opts)
                   ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^

  File "/usr/lib/python3.13/smtplib.py", line 554, in mail
    self.putcmd("mail", "from:%s%s" % (quoteaddr(sender), optionlist))
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/usr/lib/python3.13/smtplib.py", line 387, in putcmd
    self.send(f'{s}{CRLF}')
    ~~~~~~~~~^^^^^^^^^^^^^^

  File "/usr/lib/python3.13/smtplib.py", line 374, in send
    raise SMTPServerDisconnected('please run connect() first')

SMTPServerDisconnected: please run connect() first
