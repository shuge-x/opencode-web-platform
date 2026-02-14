# 完整开发流程规范（v3.0）

**更新日期**: 2026-02-14
**强制执行**: 所有人必须遵守
**核心原则**: **全自动化，零人工干预**

---

## 📋 标准流程（强制执行）

### Phase 1: 开发与提交
1. ✅ 开发代码
2. ✅ 本地测试
3. ✅ Git commit
4. ✅ **立即Git push**

### Phase 2: CI/CD自动化（**必须自动执行**）
1. ✅ **自动检测到push事件**
2. ✅ **自动触发GitHub Actions**
3. ✅ **自动启动跟踪程序**
4. ✅ **每30秒查询一次进度**
5. ✅ **自动分析每个job状态**

### Phase 3: 异常处理（**必须自动执行**）
```
如果 CI/CD失败：
  1. ✅ 自动获取失败日志
  2. ✅ 自动分析失败原因
  3. ✅ 自动定位问题代码
  4. ✅ 自动修复问题
  5. ✅ 自动重新提交
  6. ✅ 回到Phase 2继续跟踪
  7. ⚠️ 循环直到成功（最多5次）
```

### Phase 4: 成功汇报（**必须主动执行**）
```
如果 CI/CD全部通过：
  1. ✅ 自动确认所有jobs状态为success
  2. ✅ 自动生成验收报告
  3. ✅ **主动通知术哥验收**
  4. ❌ 不要等术哥问进度
```

---

## 🚨 强制规则

### 规则1：提交后必须自动跟踪
**触发条件**: Git push完成
**执行动作**: 立即启动CI/CD跟踪程序

### 规则2：失败必须自动修复
**触发条件**: 任何job失败
**执行动作**:
- 分析日志
- 定位问题
- 修复代码
- 重新push

### 规则3：成功必须主动汇报
**触发条件**: 所有jobs通过
**执行动作**: **立即通知术哥验收**
**禁止行为**: 等术哥问进度

---

## 🤖 自动化脚本

### CI/CD自动跟踪脚本
```python
#!/usr/bin/env python3
"""
自动跟踪CI/CD并处理异常
位置: scripts/auto_track_cicd.py
"""
import time
import json
import urllib.request

def track_cicd():
    """自动跟踪CI/CD进度"""
    max_attempts = 20  # 最多检查20次（10分钟）

    for i in range(max_attempts):
        # 查询CI/CD状态
        status = get_cicd_status()

        print(f"[{i+1}/{max_attempts}] 状态: {status['status']}, 结果: {status['conclusion']}")

        if status['status'] == 'completed':
            if status['conclusion'] == 'success':
                # 成功：主动汇报
                notify_success()
                return True
            else:
                # 失败：自动修复
                fixed = auto_fix_failure()
                if fixed:
                    # 修复成功，重新跟踪
                    continue
                else:
                    # 修复失败，通知术哥
                    notify_failure()
                    return False

        time.sleep(30)  # 每30秒检查一次

    # 超时
    notify_timeout()
    return False

def auto_fix_failure():
    """自动分析并修复失败"""
    # 1. 获取失败日志
    logs = get_failure_logs()

    # 2. 分析失败原因
    reason = analyze_failure(logs)

    # 3. 定位问题代码
    problem = locate_problem(reason)

    # 4. 自动修复
    fix_result = auto_fix(problem)

    # 5. 重新提交
    if fix_result:
        git_commit_and_push()
        return True

    return False

def notify_success():
    """主动汇报成功"""
    message = """
🎉 CI/CD全部通过！

✅ 后端测试: 通过
✅ 前端测试: 通过
✅ 前端构建: 通过
✅ Docker构建: 通过

📦 仓库: https://github.com/shuge-x/opencode-web-platform
📊 Actions: {最新运行链接}

🎯 项目已完全就绪，可以验收！
    """
    send_to_shuge(message)

def notify_failure():
    """通知失败（无法自动修复）"""
    message = """
❌ CI/CD失败，无法自动修复

失败原因: {详细原因}
失败日志: {日志链接}

需要人工干预。
    """
    send_to_shuge(message)

# 启动跟踪
if __name__ == "__main__":
    track_cicd()
```

---

## 📊 流程图

```
Git Push → CI/CD触发 → 自动启动跟踪程序
                              ↓
                      每30秒查询状态
                              ↓
                      ┌──────┴──────┐
                      │             │
                  运行中        已完成
                      │             │
                      ↓       ┌─────┴─────┐
                  继续查询    │           │
                            成功       失败
                              │           │
                              ↓           ↓
                        主动汇报术哥   自动修复
                                      │
                                      ↓
                                  重新Push
                                      │
                                      ↓
                                  回到起点
```

---

## ✅ 检查清单

每次提交代码后，系统必须自动执行：

- [ ] Git push完成
- [ ] **自动启动CI/CD跟踪**（30秒间隔）
- [ ] **自动检测失败**
- [ ] **自动分析原因**
- [ ] **自动修复问题**
- [ ] **自动重新提交**
- [ ] **循环直到成功**
- [ ] **成功后主动汇报术哥**

**禁止行为**：
- ❌ 等术哥问进度
- ❌ 手动查询CI/CD
- ❌ 不汇报结果

---

## 📝 改进记录

### v1.0（错误版本）
- ❌ 没有自动push
- ❌ 没有CI/CD

### v2.0（部分正确）
- ✅ 自动push
- ✅ CI/CD配置
- ❌ 手动跟踪进度
- ❌ 被动汇报结果

### v3.0（当前版本）
- ✅ 自动push
- ✅ CI/CD配置
- ✅ **自动跟踪进度**（30秒轮询）
- ✅ **自动分析异常**
- ✅ **自动修复问题**
- ✅ **主动汇报结果**

---

## 🎯 目标

**零人工干预**：
- 代码提交 → CI/CD运行 → 自动跟踪 → 异常自动修复 → 成功主动汇报

**零等待**：
- 术哥不需要问进度，完成后自动收到通知

---

## 🔧 实现方式

### 方式1：后台脚本（推荐）
```bash
# 提交代码后自动启动
git push && python3 scripts/auto_track_cicd.py
```

### 方式2：GitHub Webhook（未来）
- 监听GitHub push事件
- 自动触发跟踪脚本
- 自动处理异常

---

**负责人**: 术维斯1号
**监督**: 术哥
**强制执行**: 2026-02-14起
**目标**: 全自动化，零人工干预，主动汇报
