import React from 'react';

const surfaces={
  default:{background:'var(--bg-elevated)',border:'1px solid var(--border-subtle)',boxShadow:'var(--shadow-card)'},
  surface:{background:'var(--bg-surface)',border:'1px solid var(--border-warm)',boxShadow:'none'},
  elevated:{background:'var(--bg-elevated)',border:'1px solid var(--border-subtle)',boxShadow:'var(--shadow-raised)'},
  inverse:{background:'var(--bg-inverse)',border:'1px solid rgba(255,255,255,.14)',boxShadow:'none'}
};

export function Card({variant='default',media,eyebrow,title,children,footer,featured=false,style,...rest}){
  const inv=variant==='inverse';
  return (
    <div style={{borderRadius:'var(--radius-md)',overflow:'hidden',display:'flex',flexDirection:'column',...surfaces[variant],...(featured?{borderColor:'var(--border-brand)',borderWidth:'2px'}:null),...style}} {...rest}>
      {media&&<div style={{background:'var(--rf-warm-neutral)',aspectRatio:'16 / 10',overflow:'hidden'}}>{media}</div>}
      <div style={{padding:'var(--space-2-5)',display:'flex',flexDirection:'column',gap:'var(--space-1)',flex:1}}>
        {eyebrow&&<div style={{fontFamily:'var(--font-ui)',fontSize:'var(--text-small)',fontWeight:'var(--weight-semibold)',letterSpacing:'var(--tracking-eyebrow)',textTransform:'uppercase',color:inv?'var(--rf-green-light)':'var(--text-brand)'}}>{eyebrow}</div>}
        {title&&<h3 style={{margin:0,fontFamily:'var(--font-display)',fontSize:'var(--text-h3)',fontWeight:'var(--weight-semibold)',lineHeight:'var(--leading-tight)',color:inv?'var(--text-on-inverse)':'var(--text-heading)'}}>{title}</h3>}
        {children&&<div style={{fontFamily:'var(--font-body)',fontSize:'var(--text-base)',lineHeight:'var(--leading-body)',color:inv?'rgba(245,241,235,.82)':'var(--text-primary)'}}>{children}</div>}
        {footer&&<div style={{marginTop:'auto',paddingTop:'var(--space-2)'}}>{footer}</div>}
      </div>
    </div>
  );
}
