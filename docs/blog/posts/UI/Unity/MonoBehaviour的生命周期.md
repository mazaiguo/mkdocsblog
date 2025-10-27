---
title: MonoBehaviour的生命周期
date: 2025-10-15
categories:
  - Unity
  - Windows程序
tags:
  - Unity
  - Markdown
  - Noob
  - UI
description: MonoBehaviour的生命周期
authors:
  - JerryMa
---

# MonoBehaviour的生命周期

  [Unity3D](https://so.csdn.net/so/search?q=Unity3D&spm=1001.2101.3001.7020) 中可以给每个游戏对象添加脚本，这些脚本必须继承 MonoBehaviour，用户可以根据需要重写 MonoBehaviour 的部分生命周期函数，这些生命周期函数由系统自动调用，且调用顺序与书写顺序无关。

​    MonoBehaviour 的继承关系：MonoBehaviour→Behaviour→Component→Object.

​    MonoBehaviour 的生命周期函数主要有：

- **OnValidate**: 确认事件，脚本被加载、启用、禁用、Inspector 面板值被修改时，都会执行一次
- **Awake**：唤醒事件，只执行 1 次，游戏一开始运行就执行。
- **OnEnable**：启用事件，只执行 1 次，当脚本组件被启用的时候执行一次。
- **Start**：开始事件，只执行 1 次。
- **FixedUpdate**：固定更新事件，每隔 0.02 秒执行一次，所有物理组件相关的更新都在这个事件中处理。
- **Update**：更新事件，每帧执行 1 次。
- **LateUpdate**：稍后更新事件，每帧执行 1 次，在 Update 事件执行完毕后再执行。
- **OnGUI**：GUI渲染事件，每帧执行 2 次。
- **OnDisable**：禁用事件，只执行1 次，在 OnDestroy 事件前执行，或者当该脚本组件被禁用后，也会触发该事件。
- **OnDestroy**：销毁事件，只执行 1 次，当脚本所挂载的游戏物体被销毁时执行。

#### 2 验证

​    LifeCycle.cs 

```csharp
using UnityEngine;

public class LifeCycle : MonoBehaviour {
    // 确认事件, 脚本被加载、启用、禁用、Inspector面板值被修改时, 都会执行一次
    private void OnValidate() {
		Debug.Log("OnValidate");
	}
	// 唤醒事件，只执行 1 次，游戏一开始运行就执行
    private void Awake() {
        Debug.Log("Awake");
    }
	// 启用事件，只执行 1 次，当脚本组件被启用的时候执行一次
    private void OnEnable() {
        Debug.Log("OnEnable");
    }

	// 开始事件，只执行 1 次
    private void Start() {
        Debug.Log("Start");
    }

	// 固定更新事件，每隔 0.02 秒执行一次，所有物理组件相关的更新都在这个事件中处理
	private void FixedUpdate() {
        // Debug.Log("FixedUpdate");
    }

	// 更新事件，每帧执行 1 次
    private void Update() {
        // Debug.Log("Update");
    }
    // 稍后更新事件，每帧执行 1 次，在 Update 事件执行完毕后再执行
    private void LateUpdate () {
        // Debug.Log("LateUpdate");
    }

    // GUI渲染事件，每帧执行 2 次
    private void OnGUI () {
        // Debug.Log("OnGUI");
    }
	// 禁用事件，只执行1 次，在 OnDestroy 事件前执行，或者当该脚本组件被禁用后，也会触发该事件
	private void OnDisable () {
        Debug.Log("OnDisable");
    }
	// 销毁事件，只执行 1 次，当脚本所挂载的游戏物体被销毁时执行
	private void OnDestroy () {
        Debug.Log("OnDestroy");
    }
}
```

​    每帧都执行的日志就不放了，读者可以自行打开，这里只看下只执行几次的生命周期函数日志，如下：

![img](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/15_16_27_20_20251015-542aef4143e6c15dfedbd9d28653e89e.png)

#### 3 完整生命周期

![img](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/15_16_27_22_20251015-b33ed910a2090c219a56f49a7a184d31.png)