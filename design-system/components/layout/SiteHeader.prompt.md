Use `SiteHeader` at the top of every marketing page. Set `transparent` when it sits over a hero photograph.

```jsx
<SiteHeader nav={[{id:'home',label:'Home'},{id:'packages',label:'Packages'}]}
            active="home" phone="(225) 978-2363"
            cta={{label:'Get a quote'}} onNavigate={setPage} />
```

Nav labels are uppercase 14px semibold with .08em tracking; the active item carries a 2px green underline.
