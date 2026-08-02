const field={width:'100%',boxSizing:'border-box',minHeight:'var(--tap-min)',padding:'12px 14px',fontFamily:'var(--font-body)',fontSize:'var(--text-base)',color:'var(--text-primary)',background:'var(--bg-base)',border:'1px solid var(--border-subtle)',borderRadius:'var(--radius-sm)',outline:'none'};
const labelStyle={display:'block',fontSize:'var(--text-small)',fontWeight:600,letterSpacing:'var(--tracking-eyebrow)',textTransform:'uppercase',color:'var(--text-heading)',marginBottom:'6px'};

function Field({label,children}){return <label style={{display:'block'}}><span style={labelStyle}>{label}</span>{children}</label>;}

function BookScreen({selected,onSelect}){
  const [sent,setSent]=React.useState(false);
  if(sent) return <Section tight align="center" width="var(--container-narrow)" eyebrow="Request received"
    heading="We'll be in touch within one business day"
    lead="Christy or Jase will confirm availability for your date and send a quote with any add-ons you asked about.">
    <div style={{display:'flex',justifyContent:'center'}}><img src={ASSETS+'/icon-flag.png'} alt="" style={{height:72,opacity:.85}}/></div>
  </Section>;

  return <Section variant="surface" tight eyebrow="Get a quote" heading="Tell us about your event"
    lead="No deposit required to check a date. We'll confirm availability first, then send pricing.">
    <div style={{display:'grid',gridTemplateColumns:'1.3fr 1fr',gap:'var(--space-3)',alignItems:'start'}}>
      <form onSubmit={e=>{e.preventDefault();setSent(true);}} style={{background:'var(--bg-base)',border:'1px solid var(--border-subtle)',borderRadius:'var(--radius-md)',boxShadow:'var(--shadow-card)',padding:'var(--space-3)',display:'grid',gap:'var(--space-2)'}}>
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'var(--space-2)'}}>
          <Field label="Your name"><input style={field} defaultValue="" placeholder="Jordan Menard" /></Field>
          <Field label="Phone"><input style={field} placeholder="(225) 555-0134" /></Field>
        </div>
        <Field label="Email"><input style={field} placeholder="you@company.com" /></Field>
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'var(--space-2)'}}>
          <Field label="Event date"><input style={field} type="date" /></Field>
          <Field label="Guests"><select style={field} defaultValue="50-100"><option>Under 25</option><option>25-50</option><option>50-100</option><option>100+</option></select></Field>
        </div>
        <Field label="Venue city"><input style={field} placeholder="Baton Rouge, LA" /></Field>
        <div>
          <span style={labelStyle}>Package</span>
          <div style={{display:'flex',gap:'var(--space-1)',flexWrap:'wrap'}}>
            {PACKAGES.map(p=>{const on=p.id===selected;return <button key={p.id} type="button" onClick={()=>onSelect(p.id)}
              style={{minHeight:'var(--tap-min)',padding:'10px 18px',borderRadius:'var(--radius-pill)',cursor:'pointer',fontFamily:'var(--font-ui)',fontSize:'14px',fontWeight:600,transition:'var(--transition-color)',
                background:on?'var(--action-primary)':'transparent',color:on?'var(--text-on-brand)':'var(--text-heading)',border:'1px solid '+(on?'var(--action-primary)':'var(--border-warm)')}}>{p.name}</button>;})}
          </div>
        </div>
        <Field label="Anything else?"><textarea style={{...field,minHeight:'96px',resize:'vertical'}} placeholder="Indoor ballroom, we'd like the Feral pack for the kids' table." /></Field>
        <Button type="submit" size="lg" fullWidth>Send request</Button>
        <p style={{margin:0,fontSize:'var(--text-small)',color:'var(--text-muted)',textAlign:'center'}}>Or call {PHONE} — we answer.</p>
      </form>

      <div style={{display:'grid',gap:'var(--space-2)'}}>
        <Card variant="default" eyebrow="What happens next" title="Three steps">
          <ol style={{margin:0,paddingLeft:'18px',lineHeight:'var(--leading-body)'}}>
            <li>We confirm your date is open.</li>
            <li>You get a quote with add-ons itemized.</li>
            <li>We arrive early, set up, and run the play.</li>
          </ol>
        </Card>
        <Card variant="inverse" eyebrow="All we need" title="One outlet">Standard household power. Wifi is a plus, not a requirement.</Card>
      </div>
    </div>
  </Section>;
}
window.BookScreen=BookScreen;
