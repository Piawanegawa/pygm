# pygm Architektur

## Generators

```plantuml
hide empty members
allow_mixing

package "pygm" {
  package "generators" {
    package plothook {        
        interface PlothookGenerator {
            +generate_plothook(description: str) -> Plothook
        }        
        package impl {
            class AIPlothookGenerator {
                +init(ai_client: pygm.utils.ai.AIClient)
            }
        }
        class Plothook {
        
        }
        AIPlothookGenerator .u.|> PlothookGenerator
        PlothookGenerator .l.> Plothook : <<creates>>
    }    
  }
  package runners {
    class CLI
    class GUI
  }  
  component AIClient
  
  AIPlothookGenerator ..> AIClient : <<uses>>
  CLI ..> PlothookGenerator : uses
  GUI ..> PlothookGenerator : uses  
}
```
## ApiKey

```plantuml
hide empty members

package "pygm" {
  package utils {
    package ai {
        enum AIProviderType {
            OPENROUTER = "OPENROUTER"
        }
        class ApiKey {
            -provider_type: AIProviderType
            -api_key: str
            +__init__(provider_type: AIProviderType, api_key: str) -> None
            +get_provider_type() -> AIProviderType
            +get_api_key() -> str
        }        
        class ApiKeyManager {
            -api_keys: dict[AIProviderType, ApiKey]
            +set_api_key(provider_type: AIProviderType, api_key: ApiKey) -> None
            +get_api_key(provider_type: AIProviderType) -> ApiKey
        }
        
        ApiKeyManager ..> ApiKey : <<manages>>
        ApiKeyManager ..> AIProviderType : <<uses>>
        AIProviderType -lo ApiKey
```

## AIPrompt und AIResponse

```plantuml
hide empty members
package "pygm" {
  package utils {
    package ai {
        enum AIMessageRole {
            SYSTEM = "system"
            USER = "user"
            ASSISTANT = "assistant"
            TOOL = "tool"
        }   
        class AIMessage {
            -role: AIMessageRole
            -content: str
            +__init__(role: AIMessageRole, content: str) -> None
            +get_role() -> AIMessageRole
            +get_content() -> str
        }        
        class AIPrompt {
            -prompt_id: str
            -messages: list[AIMessage]
            -max_output_tokens: int | None
            -temperature: float | None
            +__init__(prompt_id: str, messages: list[AIMessage], max_output_tokens: int | None = None, temperature: float | None = None) -> None
            +get_prompt_id() -> str
            +get_messages() -> list[AIMessage]
            +get_max_output_tokens() -> int | None
            +get_temperature() -> float | None  
        }
        class AIPromptBuilder {
            -prompt_id: str
            -messages: list[AIMessage] = {}
            -max_output_tokens: int | None = None
            -temperature: float | None = None
            +init(prompt_id: str)
            +add_message(role: AIMessageRole, content: str): AIPromptBuilder
            +set_max_output_tokens(max_output_tokens: int): AIPromptBuilder
            +set_temperature(temperature: float): AIPromptBuilder            
            +build(): AIPrompt
        }
        class AIResponse {
            prompt_id: str
            content: str
            finish_reason: str | None = None
            error: str | None = None
            +__init__(prompt_id: str, content: str, finish_reason: str, error: str) -> None
            +get_prompt_id() -> str      
            +get_content() -> str
            +get_finish_reason() -> str | None
            +get_error() -> str | None            
       }      
       class AIResponseBuilder {
            -prompt_id: str
            -content: str
            -finish_reason: str | None = None
            -error: str | None = None
            +__init__(prompt_id: str, content: str)
            +set_finish_reason(finish_reason: str): AIResponseBuilder
            +set_error(error: str): AIResponseBuilder            
            +build(): AIResponse
        }  
       
       AIMessage -d-> AIMessageRole
       AIMessage -uo AIPrompt
       AIPromptBuilder .d.> AIPrompt : <<creates>>
       AIResponseBuilder .u.> AIResponse : <<creates>>
              AIResponse -[hidden]u- AIPrompt
    }
  }
}
```

## AIClient

```plantuml
hide empty members

package "pygm" {
  package utils {
    package ai {
        abstract AIProvider {
            -provider_type: AIProviderType
            +__init__(provider_type: AIProviderType) -> None
            +get_provider_type() -> AIProviderType
            +get_api_endpoint() -> str
            +get_available_models() -> list[str]
            +create_ai_client(config: AIClientConfig) -> AIClient
        }
        abstract AIClientConfig {
            -api_key: ApiKey
            +__init__(api_key: ApiKey) -> None
            +get_provider_type(): AIProviderType
            +get_api_key(): str
        }
        class AIClientConfigBuilder {
            -provider: AIProviderType
            -api_key: str
            +__init__(provider_type: AIProviderType): AIClientConfigBuilder
            +build(): AIClientConfig
        }        
        interface AIClient {
            +send_prompt(prompt: AIPrompt) -> AIResponse
        }
        class AIProviderFactory {
            +create_ai_provider(provider_type: AIProviderType) -> AIProvider
        }        
        package impl {
            package openrouter {
                class OpenRouterProvider {
                    +init()
                    +get_api_endpoint(): str
                    +get_available_models(): list[str]
                    +create_ai_client(config: AIClientConfig) -> AIClient
                }
                class OpenRouterClient {
                
                }
                class OpenRouterClientConfig {
                
                }
            }
        }
                
        OpenRouterProvider .u.|> AIProvider        
        OpenRouterClient .u.|> AIClient
        OpenRouterClientConfig -u-|> AIClientConfig
        AIProviderType -lo AIClientConfig
        AIProvider ..> ApiKey : <<uses>>
        AIProvider ..> AIClient : <<creates>>
        AIProviderFactory ..> AIProvider : <<creates>>
        AIClientConfigBuilder ..> AIClientConfig : <<creates>>
    }
  }
}
```