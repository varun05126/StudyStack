# 🎨 StudyStack Design System

## Color Palette

### Primary Colors
- **Primary**: `#5B4DFF` - Main brand color
- **Primary Light**: `#8B7FFF` - Hover states
- **Primary Dark**: `#3D35D4` - Active states

### Accent Colors
- **Success (Green)**: `#10B981`
- **Warning (Orange)**: `#F59E0B`
- **Danger (Red)**: `#EF4444`
- **Info (Blue)**: `#3B82F6`

### Neutral Colors
- **Text Primary**: `#1F2937` - Main text
- **Text Secondary**: `#6B7280` - Secondary text
- **Text Tertiary**: `#9CA3AF` - Muted text
- **Background Primary**: `#FFFFFF` - Main background
- **Background Secondary**: `#F9FAFB` - Card backgrounds
- **Background Tertiary**: `#F3F4F6` - Hover states
- **Border Light**: `#E5E7EB` - Primary borders
- **Border Dark**: `#D1D5DB` - Darker borders

## Typography

### Font Families
- **Headlines**: `Poppins` (700, 800, 900 weights)
- **Body**: `Inter` (300-700 weights)

### Font Sizes
- **H1**: 2.5rem (40px)
- **H2**: 2rem (32px)
- **H3**: 1.5rem (24px)
- **H4**: 1.25rem (20px)
- **Body**: 1rem (16px)
- **Small**: 0.875rem (14px)
- **Tiny**: 0.75rem (12px)

## Spacing Scale

| Name | Value |
|------|-------|
| XS   | 4px   |
| SM   | 8px   |
| MD   | 12px  |
| LG   | 16px  |
| XL   | 20px  |
| 2XL  | 24px  |
| 3XL  | 32px  |

## Border Radius

| Level | Value |
|-------|-------|
| XS    | 4px   |
| SM    | 6px   |
| MD    | 8px   |
| LG    | 12px  |
| XL    | 16px  |
| 2XL   | 20px  |

## Shadows

| Level | Usage |
|-------|-------|
| XS    | Subtle elements |
| SM    | Small cards, borders |
| MD    | Standard cards |
| LG    | Hover states |
| XL    | Modals, important elements |

## Component Usage

### Buttons

```html
<!-- Primary Button -->
<button class="btn btn-primary">Click Me</button>

<!-- Secondary Button -->
<button class="btn btn-secondary">Click Me</button>

<!-- Outlined Button -->
<button class="btn btn-outline">Click Me</button>

<!-- Small Button -->
<button class="btn btn-primary btn-sm">Small</button>

<!-- Large Button -->
<button class="btn btn-primary btn-lg">Large</button>

<!-- Danger Button -->
<button class="btn btn-danger">Delete</button>
```

### Cards

```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Card Title</h3>
  </div>
  <div class="card-body">
    <p>Card content here</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary">Action</button>
  </div>
</div>
```

### Forms

```html
<form>
  <div class="form-group">
    <label for="email">Email</label>
    <input type="email" id="email" placeholder="you@example.com">
  </div>
  
  <div class="form-group">
    <label for="message">Message</label>
    <textarea id="message" placeholder="Your message..."></textarea>
  </div>
  
  <button type="submit" class="btn btn-primary btn-lg">Submit</button>
</form>
```

### Badges

```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-danger">Danger</span>
```

### Alerts

```html
<div class="alert alert-success">
  ✓ Success message
</div>

<div class="alert alert-error">
  ✗ Error message
</div>

<div class="alert alert-warning">
  ⚠ Warning message
</div>

<div class="alert alert-info">
  ℹ Information message
</div>
```

### Grid System

```html
<!-- 2-column grid -->
<div class="grid grid-2">
  <div class="card">Item 1</div>
  <div class="card">Item 2</div>
</div>

<!-- 3-column grid -->
<div class="grid grid-3">
  <div class="stat-box">Stat 1</div>
  <div class="stat-box">Stat 2</div>
  <div class="stat-box">Stat 3</div>
</div>
```

## Dark Mode

The design system includes full dark mode support. Users can toggle via the theme button in the header. CSS variables automatically adapt:

```css
:root {
  --primary: #5B4DFF;      /* Light mode */
}

body.dark {
  --primary: #7C5FFF;      /* Dark mode */
}
```

## Responsive Breakpoints

- **Mobile**: max-width: 480px
- **Tablet**: max-width: 768px
- **Desktop**: 1200px+

## Accessibility

- ✅ WCAG 2.1 AA compliant
- ✅ Proper color contrast ratios
- ✅ Focus states on all interactive elements
- ✅ Semantic HTML structure
- ✅ Keyboard navigation support

## Performance

- ✅ CSS variables for theming
- ✅ GPU-accelerated animations
- ✅ Optimized transitions (200-300ms)
- ✅ Mobile-first approach

## Brand Voice

- **Modern**: Clean, contemporary design
- **Professional**: Trustworthy and polished
- **Approachable**: Friendly and welcoming
- **Efficient**: Fast and responsive

---

For implementation details, refer to `/static/core/style.css`
