import React from 'react';

export function Hero({eyebrow,headline,subhead,image,actions,trust=[],height=560,style,...rest}){
  return (
    <section style={{position:'relative',minHeight:height,display:'flex',alignItems:'center',background:image?'var(--rf-green-dark)':'var(--gradient-brand)',overflow:'hidden',...style}} {...rest}>
      {image&&<div style={{position:'absolute',inset:0}}>
        <div style={{position:'absolute',inset:0,backgroundImage:'url('+image+')',backgroundSize:'cover',backgroundPosition:'center'}} />
        <div style={{position:'absolute',inset:0,background:'var(--overlay-hero)'}} />
        <div style={{position:'absolute',inset:0,background:'var(--overlay-scrim)'}} />
      </div>}
      <div style={{position:'relative',maxWidth:'var(--container)',margin:'0 auto',padding:'var(--space-5) var(--gutter)',width:'100%'}}>
        {eyebrow&&<div style={{fontSize:'var(--text-small)',fontWeight:'var(--weight-semibold)',letterSpacing:'var(--tracking-eyebrow)',textTransform:'uppercase',color:'var(--rf-ivory)',opacity:.9,marginBottom:'var(--space-2)'}}>{eyebrow}</div>}
        {headline&&<h1 style={{margin:0,maxWidth:'16ch',fontFamily:'var(--font-display)',fontSize:'var(--text-display)',fontWeight:'var(--weight-light)',letterSpacing:'var(--tracking-h1)',lineHeight:'var(--leading-heading)',color:'var(--rf-white)'}}>{headline}</h1>}
        {subhead&&<p style={{margin:'var(--space-2) 0 0',maxWidth:'52ch',fontSize:'18px',lineHeight:'var(--leading-body)',color:'var(--rf-ivory)'}}>{subhead}</p>}
        {actions&&<div style={{display:'flex',flexWrap:'wrap',gap:'var(--space-2)',marginTop:'var(--space-3)'}}>{actions}</div>}
        {trust.length>0&&<ul style={{display:'flex',flexWrap:'wrap',gap:'var(--space-3)',listStyle:'none',margin:'var(--space-4) 0 0',padding:0}}>
          {trust.map((t,i)=><li key={i} style={{fontSize:'var(--text-small)',fontWeight:'var(--weight-semibold)',letterSpacing:'var(--tracking-eyebrow)',textTransform:'uppercase',color:'var(--rf-ivory)',opacity:.85}}>{t}</li>)}
        </ul>}
      </div>
    </section>
  );
}
