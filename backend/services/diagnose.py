"""StellarPulse - AI Diagnosis Service."""

import asyncio
from typing import List, Optional


async def diagnose_issue(
    alert_id: Optional[int] = None,
    target_type: Optional[str] = None,
    target_name: Optional[str] = None,
    symptoms: str = ""
) -> dict:
    """Diagnose issue using AI."""

    # Build diagnosis prompt
    prompt = f"""你是一个资深的SRE工程师。请根据以下症状进行故障诊断：

症状描述: {symptoms}

"""

    if target_type:
        prompt += f"故障目标类型: {target_type}\n"
    if target_name:
        prompt += f"故障目标名称: {target_name}\n"

    prompt += """
请分析可能的原因并给出：
1. 根因分析
2. 排查步骤
3. 建议的解决方案

请用中文回答，结构化输出。
"""

    try:
        from services.nanobot_client import chat_with_nanobot

        response = await chat_with_nanobot(
            prompt,
            session_id=f"diagnose:{alert_id or 'manual'}"
        )

        # Parse response
        diagnosis_text = response

        # Extract structured info (simplified)
        return {
            "diagnosis": diagnosis_text,
            "root_cause": _extract_root_cause(diagnosis_text),
            "suggestions": _extract_suggestions(diagnosis_text),
            "related_cases": []  # Could query knowledge base
        }

    except Exception as e:
        return {
            "diagnosis": f"诊断服务错误: {str(e)}",
            "root_cause": None,
            "suggestions": ["检查nanobot配置", "查看系统日志"],
            "related_cases": []
        }


def _extract_root_cause(text: str) -> Optional[str]:
    """Extract root cause from text."""
    # Simple extraction - look for keywords
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if '根因' in line or '原因' in line:
            if i + 1 < len(lines):
                return lines[i + 1].strip()
    return None


def _extract_suggestions(text: str) -> List[str]:
    """Extract suggestions from text."""
    suggestions = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith(('1.', '2.', '3.', '4.', '5.')):
            suggestions.append(line[3:].strip())
    return suggestions[:5]  # Limit to 5
