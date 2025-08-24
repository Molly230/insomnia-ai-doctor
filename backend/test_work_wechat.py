#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试企业微信配置和API连接
"""

from app.services.work_wechat_service import WorkWeChatService
from config import Config

def test_work_wechat():
    print("🚀 测试企业微信配置...")
    print(f"企业ID: {Config.WORK_WECHAT_CORP_ID}")
    print(f"应用ID: {Config.WORK_WECHAT_AGENT_ID}")
    print(f"Token: {Config.WORK_WECHAT_TOKEN}")
    print("-" * 50)
    
    # 创建服务实例
    service = WorkWeChatService()
    
    # 测试获取access_token
    print("📡 测试获取access_token...")
    access_token = service.get_access_token()
    
    if access_token:
        print(f"✅ 获取access_token成功: {access_token[:20]}...")
        
        # 测试发送消息
        print("\n📨 测试发送消息...")
        test_userid = "WuYuFang"
        test_message = "🎉 企业微信中医分身测试成功！\n\n🔹 API连接正常\n🔹 可以发送消息\n🔹 准备开始问诊功能"
        
        success = service.send_text_message(test_userid, test_message)
        if success:
            print("✅ 消息发送成功！请检查你的企业微信")
            print("   如果收到消息，说明基础功能完全正常")
        else:
            print("❌ 消息发送失败，请检查UserID或权限设置")
            
        # 测试发送Markdown消息
        print("\n📱 测试发送Markdown消息...")
        markdown_msg = """# 🌙 失眠中医分身
        
## ✅ 系统状态
- API连接：正常
- 消息发送：正常  
- 准备就绪：是

## 🔄 下一步
回复**"开始问诊"**测试19题问诊流程！"""
        
        md_success = service.send_markdown_message(test_userid, markdown_msg)
        print(f"Markdown消息发送结果: {'✅ 成功' if md_success else '❌ 失败'}")
        
    else:
        print("❌ 获取access_token失败，请检查配置")
        print("   1. 确认企业ID是否正确")
        print("   2. 确认应用Secret是否正确")
        print("   3. 确认网络连接正常")

if __name__ == '__main__':
    test_work_wechat()