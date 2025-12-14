# pygm Architektur

## Überblick

```plantuml
hide empty members

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
        AIPlothookGenerator ..> pygm.utils.ai.AIClient : <<uses>>
        AIPlothookGenerator ..> pygm.utils.ai.AIClientConfig : <<uses>>
        AIPlothookGenerator ..> pygm.utils.ai.AIClientFactory : <<uses>>
    }    
  }
  package runners {
    class CLI
    class GUI
  }
  package utils {
    package ai {
        interface AIClient
        abstract AIClientConfig {
            -model: AIAccessType
            +get_access_type() : AIAccessType
        }
        enum AIAccessType {
            LITELLM
        }
        class AIClientFactory {
            +create_ai_client(config: AIClientConfig) -> AIClient
        }
        class AIClientConfigBuilder {
            +set_openrouter_config() -> AIClientConfigBuilder
            +build() -> AIClientConfig
        }
        package impl {
            package litellm {
                class LiteLLMClient {
                
                }
                class LiteLLMClientConfig {
                
                }
            }
        }        
        LiteLLMClient .u.|> AIClient
        LiteLLMClientConfig -u-|> AIClientConfig
        AIClientFactory ..> AIClientConfig : <<uses>>
        AIClientFactory ..> AIClient : <<creates>>
    }
  }
  
  CLI ..> PlothookGenerator : uses
  GUI ..> PlothookGenerator : uses  
}
```