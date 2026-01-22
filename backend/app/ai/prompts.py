"""
AI 提示词模板
"""

ORDER_ANALYSIS_PROMPT = """你是一个物料供应链分析助手。请根据以下订单信息，分析最佳的履行方式。

## 订单信息
{order_info}

## 合同厂家信息
{contract_manufacturer_info}

## 可用的替代厂家
{alternative_suppliers}

## 分析要求
1. 判断合同厂家是否能直接供应所有产品
2. 如果不能，分析是否需要委托供货或委托加工
3. 给出具体的履行建议

请用中文回答，格式如下：
- 履行方式：[直接发货/委托供货/委托加工]
- 分析原因：...
- 具体建议：...
- 预计完成时间：...
"""

DELEGATION_ADVICE_PROMPT = """你是一个委托函起草助手。请根据以下信息，帮助生成委托函内容。

## 委托类型
{delegation_type}

## 订单信息
{order_info}

## 委托方信息（合同厂家）
{delegator_info}

## 被委托方信息（第三方厂家）
{delegatee_info}

## 委托金额
{amount}

## 额外说明
{additional_info}

请生成一份正式的委托函内容，包括：
1. 委托事项说明
2. 产品/服务要求
3. 交付要求
4. 付款条款
5. 其他约定事项

请用正式的商务语言撰写。
"""

SUPPLY_CHAIN_OPTIMIZATION_PROMPT = """你是一个供应链优化助手。请根据以下历史订单和供应数据，给出优化建议。

## 历史订单数据
{order_history}

## 厂家供应能力
{supplier_capacity}

## 当前问题
{current_issues}

请分析并给出以下方面的建议：
1. 供应商选择优化
2. 库存管理建议
3. 采购时机建议
4. 成本优化方案
"""

PRODUCT_MATCHING_PROMPT = """你是一个产品匹配助手。请根据用户需求，从产品库中匹配最合适的产品。

## 用户需求描述
{user_requirement}

## 可用产品列表
{available_products}

请返回最匹配的产品列表，并说明匹配原因。格式如下：
1. 产品名称 - 匹配度：高/中/低 - 原因：...
"""
