# Visual Design Guide

## 🎨 Design System Overview

### Color Palette
```
Primary Gradient: #667eea → #764ba2 (Purple to Pink)
Success Gradient: #11998e → #38ef7d (Teal to Green)
Danger Gradient:  #ee0979 → #ff6a00 (Pink to Orange)
Warning Gradient: #f093fb → #f5576c (Pink to Red)
```

### Design Principles
- **Glassmorphism**: Semi-transparent cards with backdrop blur
- **3D Effects**: Depth through shadows and transforms
- **Animations**: Smooth transitions and hover effects
- **Consistency**: Same design language across all pages

---

## 📄 Page Layouts

### 1. Login Page
```
┌─────────────────────────────────────────┐
│     [Animated Background Particles]     │
│                                         │
│         ┌─────────────────┐            │
│         │  [3D Shield]    │            │
│         │  Welcome Back   │            │
│         │                 │            │
│         │  [Username]     │            │
│         │  [Password]     │            │
│         │  [Login Button] │            │
│         │                 │            │
│         │  Create Account │            │
│         │  Demo Creds     │            │
│         └─────────────────┘            │
│                                         │
└─────────────────────────────────────────┘
```

**Features**:
- Floating animated particles
- 3D shield icon with pulse animation
- Glassmorphism login card
- Mouse-tracking tilt effect
- Gradient input fields with glow

---

### 2. Dashboard
```
┌─────────────────────────────────────────────────────────┐
│  [Navbar: Logo | Dashboard | Admin | Monitor | Upload] │
├─────────────────────────────────────────────────────────┤
│                   AI Dashboard                          │
│         Real-time Exam Monitoring & Analytics           │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  [Icon]  │  │  [Icon]  │  │  [Icon]  │            │
│  │  Total   │  │  Active  │  │  System  │            │
│  │  Detect  │  │   Days   │  │  Status  │            │
│  │   123    │  │    45    │  │  ACTIVE  │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐            │
│  │  Risk Level     │  │  Detection      │            │
│  │  [Progress Bar] │  │  [Chart]        │            │
│  └─────────────────┘  └─────────────────┘            │
│                                                         │
│  ┌─────────────────────────────────────┐              │
│  │  Recent Alerts                      │              │
│  │  ┌───────────────────────────────┐ │              │
│  │  │ [Time] [Behaviors] [View Btn] │ │              │
│  │  └───────────────────────────────┘ │              │
│  └─────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

**Features**:
- 3D stat cards with hover tilt
- Animated rotating icons
- Gradient progress bars
- Interactive charts
- Auto-refreshing statistics

---

### 3. Live Monitor (Enhanced)
```
┌─────────────────────────────────────────────────────────┐
│  [Navbar: Logo | Dashboard | Admin | Monitor | Upload] │
├─────────────────────────────────────────────────────────┤
│                   Live Monitor                          │
│         Real-time exam monitoring with AI detection     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │  Camera Feed    [Test] [Start] [Stop]          │  │
│  │  ┌─────────────────────────────────────────┐   │  │
│  │  │                                         │   │  │
│  │  │        [Live Video Stream]              │   │  │
│  │  │        or                               │   │  │
│  │  │        [Camera Icon]                    │   │  │
│  │  │        Click "Start" to begin           │   │  │
│  │  │                                         │   │  │
│  │  └─────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────┐  ┌─────────────────────┐    │
│  │  Detection Status   │  │  Recent Alerts      │    │
│  │  Status: [ACTIVE]   │  │  ┌───────────────┐  │    │
│  │  Last: [Time]       │  │  │ [Alert Card]  │  │    │
│  │                     │  │  └───────────────┘  │    │
│  └─────────────────────┘  └─────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**Features**:
- 3D video card with rounded corners
- Gradient control buttons
- Pulsing status badges
- Animated alert cards
- Real-time updates every 3s

---

### 4. Video Upload (NEW)
```
┌─────────────────────────────────────────────────────────┐
│  [Navbar: Logo | Dashboard | Admin | Monitor | Upload] │
├─────────────────────────────────────────────────────────┤
│                   Video Upload                          │
│      Upload exam recordings for AI-powered detection    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │                                                 │  │
│  │         [Floating Video Icon]                   │  │
│  │         Drop Video Here                         │  │
│  │         or click to browse                      │  │
│  │         Supported: MP4, AVI, MOV...            │  │
│  │         [Browse Files Button]                   │  │
│  │                                                 │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  [Progress Bar - shown during upload]                  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │  Analysis Complete                              │  │
│  │  ┌──────┐  ┌──────┐  ┌──────┐                 │  │
│  │  │Total │  │Susp. │  │Risk  │                 │  │
│  │  │Frames│  │Frames│  │Level │                 │  │
│  │  └──────┘  └──────┘  └──────┘                 │  │
│  │                                                 │  │
│  │  Detected Behaviors                             │  │
│  │  [Behavior cards with counts]                   │  │
│  │                                                 │  │
│  │  Detection Timeline                             │  │
│  │  ┌───────────────────────────────────────┐     │  │
│  │  │ Frame 120 (2:00) [Behaviors] [View]  │     │  │
│  │  └───────────────────────────────────────┘     │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Features**:
- Drag & drop upload zone
- Animated floating icon
- Real-time progress bar
- Comprehensive results display
- Timeline with timestamps
- Evidence screenshot links

---

## 🎭 Animation Types

### 1. Float Animation
```css
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-15px); }
}
```
**Used for**: Icons, titles, particles

### 2. Pulse Animation
```css
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}
```
**Used for**: Status badges, icons

### 3. Glow Animation
```css
@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(..., 0.5); }
    50% { box-shadow: 0 0 40px rgba(..., 0.8); }
}
```
**Used for**: Progress bars, buttons

### 4. Slide-in Animation
```css
@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}
```
**Used for**: Alerts, cards

### 5. 3D Tilt Effect
```javascript
card.addEventListener('mousemove', (e) => {
    // Calculate rotation based on mouse position
    const rotateX = (y - centerY) / 20;
    const rotateY = (centerX - x) / 20;
    card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
});
```
**Used for**: All cards on mouse hover

---

## 🎯 Interactive Elements

### Buttons
```
┌─────────────────┐
│  [Icon] TEXT    │  ← Gradient background
│                 │  ← Hover: lift up 3px
│                 │  ← Active: lift up 1px
└─────────────────┘  ← Box shadow for depth
```

**States**:
- Normal: Gradient + shadow
- Hover: Lift + stronger shadow
- Active: Slight lift
- Disabled: Opacity 50%

### Cards
```
┌─────────────────────┐
│  [Glassmorphism]    │  ← Semi-transparent
│  backdrop-blur      │  ← Blurred background
│  border glow        │  ← Subtle border
│  content            │  ← White text
└─────────────────────┘  ← Multiple shadows
```

**Effects**:
- Hover: Lift up 10px
- Mouse move: 3D tilt
- Transition: Smooth 0.3s

### Status Badges
```
┌──────────────┐
│ ● ACTIVE     │  ← Pulsing animation
└──────────────┘  ← Gradient background
                  ← Glowing shadow
```

**Types**:
- Active: Green gradient
- Inactive: Red gradient
- Processing: Blue gradient

---

## 📱 Responsive Breakpoints

```
Desktop:  > 992px  (Full layout)
Tablet:   768-992px (Adjusted columns)
Mobile:   < 768px  (Stacked layout)
```

**Adaptations**:
- Cards stack vertically on mobile
- Buttons become full-width
- Font sizes scale down
- Navigation collapses to hamburger

---

## 🎨 Component Library

### Glassmorphism Card
```css
background: rgba(255, 255, 255, 0.15);
backdrop-filter: blur(20px);
border-radius: 25px;
border: 1px solid rgba(255, 255, 255, 0.2);
box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
```

### Gradient Button
```css
background: linear-gradient(135deg, #667eea, #764ba2);
border-radius: 20px;
box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
transition: all 0.3s ease;
```

### Behavior Badge
```css
background: linear-gradient(135deg, #ee0979, #ff6a00);
border-radius: 20px;
padding: 5px 15px;
box-shadow: 0 5px 15px rgba(238, 9, 121, 0.4);
```

---

## 🌟 Special Effects

### Particle Background (Login)
- 5 floating circles
- Different sizes and positions
- Infinite float animation
- Semi-transparent white

### Video Feed Overlay
- Black background
- Rounded corners
- Inner shadow for depth
- Smooth fade transitions

### Progress Bar
- Gradient fill animation
- Glowing effect
- Percentage text overlay
- Smooth width transitions

---

**Design Philosophy**: Modern, clean, professional with playful animations that enhance UX without being distracting.
