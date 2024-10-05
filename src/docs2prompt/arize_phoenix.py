from phoenix.otel import register

## OpenAI Instrumentation
def openai_instrumentation():

    tracer_provider = register(
        project_name="docs2prompt",
        endpoint="http://localhost:6006/v1/traces"
    )
    from openinference.instrumentation.openai import OpenAIInstrumentor 
    OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

## 
# from arize_otel import register_otel, Endpoints
# register_otel(
#     endpoints = Endpoints.LOCAL_PHOENIX_HTTP,
#     space_id = "docs2prompt", # in app space settings page
#     api_key = "your-api-key", # in app space settings page
#     model_id = "your-model-id", # name this to whatever you would like
# )

## https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-litellm
# import phoenix as px
# session = px.launch_app()
# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import SimpleSpanProcessor
# from openinference.instrumentation.litellm import LiteLLMInstrumentor
# endpoint = "http://localhost:6006/v1/traces"
# tracer_provider = TracerProvider()
# tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
# LiteLLMInstrumentor().instrument(tracer_provider=tracer_provider)
