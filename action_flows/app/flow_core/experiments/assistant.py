class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            user_id = configuration.get("user_id", None)
            state = {**state, "user_info": user_id}
            result = self.runnable.invoke(state)
            # Re-prompt if LLM returns an empty response
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}