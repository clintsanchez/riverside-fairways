import React from 'react';
import {Logo} from '../core/Logo.jsx';

export function SiteFooter({columns=[],phone,email,serviceArea,social=[],tagline='Bringing the fairway to you',basePath='assets',style,...rest}){
  const link={color:'var(--rf-ivory)',opacity:.8,textDecoration:'none',fontSize:'var(--text-base)',lineHeight:2};
  return (
    <footer style={{background:'var(--bg-inverse)',color:'var(--text-on-inverse)',padding:'var(--space-4) var(--gutter) var(--space-3)',...style}} {...rest}>
      <div style={{maxWidth:'var(--container)',margin:'0 auto',display:'grid',gridTemplateColumns:'1.4fr repeat('+Math.max(columns.length,1)+',1fr)',gap:'var(--space-3)'}}>
        <div>
          <Logo variant="ivory" height={72} basePath={basePath} />
          <p style={{margin:'var(--space-2) 0 0',fontSize:'var(--text-small)',letterSpacing:'var(--tracking-eyebrow)',textTransform:'uppercase',color:'var(--rf-green-light)'}}>{tagline}</p>
          {serviceArea&&<p style={{margin:'var(--space-2) 0 0',fontSize:'14px',lineHeight:'var(--leading-body)',opacity:.8,maxWidth:'34ch'}}>{serviceArea}</p>}
        </div>
        {columns.map(col=>(
          <div key={col.title}>
            <div style={{fontSize:'var(--text-small)',fontWeight:'var(--weight-semibold)',letterSpacing:'var(--tracking-eyebrow)',textTransform:'uppercase',color:'var(--rf-green-light)',marginBottom:'var(--space-1)'}}>{col.title}</div>
            {col.links.map(l=><div key={l.label}><a href={l.href||'#'} style={link}>{l.label}</a></div>)}
          </div>
        ))}
      </div>
      <div style={{maxWidth:'var(--container)',margin:'var(--space-3) auto 0',paddingTop:'var(--space-2)',borderTop:'1px solid rgba(245,241,235,.18)',display:'flex',flexWrap:'wrap',gap:'var(--space-2)',alignItems:'center',fontSize:'var(--text-small)',opacity:.75}}>
        <span>© {new Date().getFullYear()} Riverside Fairways</span>
        {phone&&<a href={'tel:'+phone.replace(/[^0-9+]/g,'')} style={{color:'var(--rf-ivory)',textDecoration:'none'}}>{phone}</a>}
        {email&&<a href={'mailto:'+email} style={{color:'var(--rf-ivory)',textDecoration:'none'}}>{email}</a>}
        <span style={{marginLeft:'auto',display:'flex',gap:'var(--space-2)'}}>{social.map(s=><a key={s.label} href={s.href} style={{color:'var(--rf-ivory)',textDecoration:'none'}}>{s.label}</a>)}</span>
      </div>
    </footer>
  );
}
