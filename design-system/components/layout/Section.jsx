import React from 'react';

const skins={
  default:{background:'var(--bg-base)',color:'var(--text-primary)'},
  surface:{background:'var(--bg-surface)',color:'var(--text-primary)'},
  subtle:{background:'var(--bg-subtle)',color:'var(--text-primary)'},
  inverse:{background:'var(--bg-inverse)',color:'var(--text-on-inverse)'},
  brand:{background:'var(--bg-brand)',color:'var(--text-on-brand)'}
};

export function Section({variant='default',eyebrow,heading,lead,align='left',tight=false,width='var(--container)',children,style,...rest}){
  const dark=variant==='inverse'||variant==='brand';
  return (
    <section style={{padding:(tight?'var(--section-y-tight)':'var(--section-y)')+' var(--gutter)',...skins[variant],...style}} {...rest}>
      <div style={{maxWidth:width,margin:'0 auto'}}>
        {(eyebrow||heading||lead)&&(
          <header style={{textAlign:align,maxWidth:align==='center'?'var(--container-narrow)':'none',margin:align==='center'?'0 auto':0,marginBottom:'var(--space-3)'}}>
            {eyebrow&&<div style={{fontSize:'var(--text-small)',fontWeight:'var(--weight-semibold)',letterSpacing:'var(--tracking-eyebrow)',textTransform:'uppercase',color:dark?'var(--rf-green-light)':'var(--text-brand)',marginBottom:'var(--space-1)'}}>{eyebrow}</div>}
            {heading&&<h2 style={{margin:0,fontFamily:'var(--font-display)',fontSize:'var(--text-h2)',fontWeight:'var(--weight-semibold)',letterSpacing:'var(--tracking-h2)',lineHeight:'var(--leading-heading)',color:dark?'var(--rf-white)':'var(--text-heading)'}}>{heading}</h2>}
            {lead&&<p style={{margin:'var(--space-2) 0 0',fontSize:'var(--text-base)',lineHeight:'var(--leading-body)',maxWidth:'var(--measure)',marginLeft:align==='center'?'auto':0,marginRight:align==='center'?'auto':0,color:dark?'rgba(245,241,235,.85)':'var(--text-primary)'}}>{lead}</p>}
          </header>
        )}
        {children}
      </div>
    </section>
  );
}
