import json
import random
import datetime
from typing import Dict, List, Tuple

class KnowledgeBase:
    """模拟知识库管理"""
    
    def __init__(self):
        # 模拟非结构化文档知识库
        self.knowledge_base = {
            "退货政策": "商品签收后7天内可无理由退货，需保持商品完好",
            "运费说明": "订单满99元包邮，不满99元收取10元运费",
            "会员权益": "会员享受95折优惠，每月有专属优惠券",
            "发票申请": "下单时勾选需要发票，我们会在发货后7个工作日内寄出",
            "商品保修": "电子产品享受一年保修，需提供购买凭证"
        }
        
        # 用户历史问答记录
        self.history_records = []
    
    def traditional_search(self, query: str) -> str:
        """传统关键词匹配搜索（模拟低准确率）"""
        matched_keys = []
        for key in self.knowledge_base.keys():
            if any(word in query for word in key):
                matched_keys.append(key)
        
        if matched_keys:
            # 随机返回一个匹配结果，模拟65%准确率
            if random.random() < 0.65:
                selected_key = random.choice(matched_keys)
                return self.knowledge_base[selected_key]
        
        return "抱歉，没有找到相关信息"
    
    def semantic_search(self, query: str) -> str:
        """基于语义理解的智能搜索（模拟高准确率）"""
        # 模拟大模型语义理解 - 实际项目中会调用大模型API
        intent_map = {
            "退货": "退货政策",
            "退款": "退货政策",
            "运费": "运费说明",
            "邮费": "运费说明",
            "会员": "会员权益",
            "VIP": "会员权益",
            "发票": "发票申请",
            "保修": "商品保修",
            "维修": "商品保修"
        }
        
        # 简单的意图识别
        detected_intent = None
        for keyword, intent in intent_map.items():
            if keyword in query:
                detected_intent = intent
                break
        
        if detected_intent and detected_intent in self.knowledge_base:
            # 模拟89%准确率
            if random.random() < 0.89:
                return self.knowledge_base[detected_intent]
        
        return self.traditional_search(query)

class AgentWorkflow:
    """模拟基于用户意图的Agent工作流"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.satisfaction_scores = []
    
    def process_query(self, query: str, user_id: str) -> Tuple[str, float]:
        """处理用户查询并返回答案和处理时长"""
        start_time = datetime.datetime.now()
        
        # 步骤1：意图识别
        intent = self._detect_intent(query)
        
        # 步骤2：知识检索（使用语义搜索）
        answer = self.kb.semantic_search(query)
        
        # 步骤3：记录处理时长
        end_time = datetime.datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # 步骤4：记录历史
        record = {
            "user_id": user_id,
            "query": query,
            "answer": answer,
            "intent": intent,
            "timestamp": start_time.isoformat(),
            "processing_time": processing_time
        }
        self.kb.history_records.append(record)
        
        return answer, processing_time
    
    def _detect_intent(self, query: str) -> str:
        """简单的意图检测"""
        intents = ["退货退款", "运费咨询", "会员服务", "发票问题", "商品保修", "其他"]
        
        # 简单的关键词匹配
        keywords = {
            "退货退款": ["退货", "退款", "退钱", "退换"],
            "运费咨询": ["运费", "邮费", "快递费", "包邮"],
            "会员服务": ["会员", "VIP", "优惠", "折扣"],
            "发票问题": ["发票", "收据", "报销"],
            "商品保修": ["保修", "维修", "坏了", "故障"]
        }
        
        for intent, words in keywords.items():
            if any(word in query for word in words):
                return intent
        
        return "其他"
    
    def collect_feedback(self, score: int) -> None:
        """收集用户满意度评分"""
        if 1 <= score <= 5:
            self.satisfaction_scores.append(score)
    
    def get_metrics(self) -> Dict:
        """获取项目指标"""
        if not self.satisfaction_scores:
            avg_score = 0
        else:
            avg_score = sum(self.satisfaction_scores) / len(self.satisfaction_scores)
        
        return {
            "total_queries": len(self.kb.history_records),
            "avg_satisfaction": round(avg_score, 2),
            "avg_processing_time": self._calculate_avg_processing_time()
        }
    
    def _calculate_avg_processing_time(self) -> float:
        """计算平均处理时长"""
        if not self.kb.history_records:
            return 0
        
        total_time = sum(record["processing_time"] for record in self.kb.history_records)
        return round(total_time / len(self.kb.history_records), 3)

def main():
    """主函数 - 模拟智能客服知识库优化项目"""
    print("=== 智能客服知识库优化系统 ===")
    print("模拟企业级AI产品从需求洞察到落地的全流程\n")
    
    # 初始化知识库和Agent工作流
    kb = KnowledgeBase()
    agent = AgentWorkflow(kb)
    
    # 模拟用户查询场景
    test_queries = [
        ("我想退货怎么办？", "user_001"),
        ("运费怎么算？", "user_002"),
        ("会员有什么优惠？", "user_003"),
        ("怎么开发票？", "user_004"),
        ("手机坏了能保修吗？", "user_005")
    ]
    
    print("开始处理用户查询...")
    print("-" * 50)
    
    # 处理每个查询
    for query, user_id in test_queries:
        print(f"用户[{user_id}]查询: {query}")
        
        # 使用Agent工作流处理查询
        answer, processing_time = agent.process_query(query, user_id)
        
        print(f"系统回答: {answer}")
        print(f"处理时长: {processing_time:.3f}秒")
        
        # 模拟用户反馈（随机生成满意度评分）
        feedback_score = random.randint(3, 5)  # 模拟较高满意度
        agent.collect_feedback(feedback_score)
        print(f"用户评分: {feedback_score}/5")
        print("-" * 50)
    
    # 展示项目成果
    print("\n=== 项目成果展示 ===")
    metrics = agent.get_metrics()
    
    print(f"1. 知识匹配准确率提升: 65% → 89% (模拟)")
    print(f"2. 问答满意度平均分: {metrics['avg_satisfaction']}/5")
    print(f"3. 平均处理时长: {metrics['avg_processing_time']}秒")
    
    # 模拟处理时长缩短效果
    baseline_time = 0.5  # 基准处理时长
    improvement = (baseline_time - metrics['avg_processing_time']) / baseline_time * 100
    print(f"4. 客服平均处理时长缩短: {max(0, improvement):.1f}% (模拟)")
    
    print(f"\n总处理查询数: {metrics['total_queries']}")
    print("项目模拟完成！")

if __name__ == "__main__":
    main()