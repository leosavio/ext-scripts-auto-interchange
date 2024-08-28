# MADR 1.0.0 - Decisão de Arquitetura para Uso de AWS Batch com EC2

* Status: Aceito
* Data: 28/08/2024

## Contexto e Problema

Para a execução de workloads resilientes e críticos na AWS utilizando AWS Batch, precisamos definir a melhor estratégia de provisionamento e uso de instâncias EC2. O objetivo é garantir a resiliência para jobs que podem tolerar interrupções e assegurar que jobs críticos que não podem ser interrompidos sejam executados de forma consistente. Além disso, o tempo de inicialização das instâncias (cold start) foi considerado, uma vez que um tempo de 3 minutos é aceitável para os workloads planejados. Todos os jobs serão desenvolvidos em Java e devemos considerar estratégias para um encerramento gracioso (graceful shutdown) de jobs resilientes ao identificar a interrupção de instâncias Spot.

## Decisão

Optamos por utilizar um ambiente de computação (Compute Environment) no AWS Batch rodando em instâncias EC2, com as seguintes estratégias:

1. Para jobs que possuem resiliência a interrupções, o ambiente de computação utilizará instâncias EC2 Spot. 
2. Para jobs que precisam de execução garantida até o fim, o ambiente de computação utilizará instâncias EC2 On-Demand.

Em ambos os cenários, as instâncias serão provisionadas sob demanda (on demand). O tempo de cold start de até 3 minutos foi considerado aceitável para os workloads.

## Consequências

### Positivas

- **Custo-eficiência:** O uso de instâncias Spot para jobs resilientes reduz os custos de computação, aproveitando o modelo de preços dinâmico da AWS.
- **Flexibilidade:** A configuração permite que workloads com diferentes níveis de criticidade sejam tratados de forma adequada, otimizando tanto custo quanto performance.
- **Padronização:** A utilização do módulo Terraform [terraform-aws-batch](https://github.com/terraform-aws-modules/terraform-aws-batch) garante uma padronização na criação dos ambientes de computação e definições de jobs em todas as contas da AWS com capacidade de execução de jobs.

### Negativas

- **Gerenciamento de Interrupções:** É necessário desenvolver uma estratégia de shutdown gracioso para os jobs que rodam em instâncias Spot, identificando quando a AWS sinaliza a interrupção da instância.
- **Complexidade:** O desenvolvimento de estratégias de shutdown gracioso pode adicionar complexidade adicional no código dos jobs, exigindo uma lógica específica para lidar com a interrupção de instâncias Spot.

## Implementação

A criação dos ambientes de computação será realizada utilizando o módulo Terraform mencionado anteriormente. Este módulo será responsável pela criação das definições de jobs e dos ambientes de computação, assegurando que as políticas de resiliência e de provisionamento sob demanda sejam aplicadas corretamente.

## Referências

- [AWS Batch - Compute Environments](https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html)
- [Terraform AWS Batch Module](https://github.com/terraform-aws-modules/terraform-aws-batch)

