import React from 'react';
import {Logo} from '../core/Logo.jsx';
import {Button} from '../core/Button.jsx';

export function SiteHeader({nav=[],active,onNavigate,phone,cta,basePath='assets',transparent=false,style,...rest}){
  return (
    <header style={{position:'relative',zIndex:5,background:transparent?'transparent':'var(--bg-base)',borderBottom:transparent?'1px solid rgba(255,255,255,.18)':'1px solid var(--border-subtle)',...style}} {...rest}>
      <div style={{maxWidth:'var(--container)',margin:'0 auto',padding:'var(--space-2) var(--gutter)',display:'flex',alignItems:'center',gap:'var(--space-3)'}}>
        <a href="#" onClick={e=>{e.preventDefault();onNavigate&&onNavigate(nav[0]&&nav[0].id);}} style={{display:'block',textDecoration:'none'}}>
          <Logo variant={transparent?'reversed':'primary'} height={52} basePath={basePath} />
        </a>
        <nav style={{display:'flex',gap:'var(--space-2-5)',marginLeft:'auto'}}>
          {nav.map(item=>{
            const on=item.id===active;
            return <a key={item.id} href={'#'+item.id} onClick={e=>{e.preventDefault();onNavigate&&onNavigate(item.id);}}
              style={{fontFamily:'var(--font-ui)',fontSize:'14px',fontWeight:'var(--weight-semibold)',letterSpacing:'.08em',textTransform:'uppercase',textDecoration:'none',paddingBottom:'2px',borderBottom:'2px solid '+(on?'var(--action-primary)':'transparent'),color:transparent?'var(--rf-white)':(on?'var(--text-brand)':'var(--text-heading)'),transition:'var(--transition-color)'}}>{item.label}</a>;
          })}
        </nav>
        {phone&&<a href={'tel:'+phone.replace(/[^0-9+]/g,'')} style={{fontFamily:'var(--font-ui)',fontSize:'14px',fontWeight:'var(--weight-semibold)',textDecoration:'none',color:transparent?'var(--rf-ivory)':'var(--text-heading)'}}>{phone}</a>}
        {cta&&<Button variant={transparent?'reversed':'primary'} onClick={cta.onClick}>{cta.label}</Button>}
      </div>
    </header>
  );
}
