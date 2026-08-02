import React from 'react';

const base={display:'inline-flex',alignItems:'center',justifyContent:'center',gap:'var(--space-1)',fontFamily:'var(--font-ui)',fontWeight:'var(--weight-semibold)',letterSpacing:'.04em',textDecoration:'none',cursor:'pointer',border:'2px solid transparent',borderRadius:'var(--radius-sm)',transition:'var(--transition-color)',minHeight:'var(--tap-min)',lineHeight:1};

const sizes={
  md:{fontSize:'15px',padding:'12px 26px'},
  lg:{fontSize:'17px',padding:'16px 38px',minHeight:'52px'},
  sm:{fontSize:'13px',padding:'9px 18px',minHeight:'38px'}
};

const variants={
  primary:{background:'var(--action-primary)',color:'var(--text-on-brand)',borderColor:'var(--action-primary)'},
  outline:{background:'transparent',color:'var(--text-brand)',borderColor:'var(--action-primary)'},
  ghost:{background:'transparent',color:'var(--text-heading)',borderColor:'transparent',padding:'12px 12px'},
  reversed:{background:'var(--rf-white)',color:'var(--text-brand)',borderColor:'var(--rf-white)'}
};

const hovers={
  primary:{background:'var(--action-primary-hover)',borderColor:'var(--action-primary-hover)'},
  outline:{background:'var(--action-primary)',color:'var(--text-on-brand)'},
  ghost:{color:'var(--text-brand)'},
  reversed:{background:'var(--rf-ivory)',borderColor:'var(--rf-ivory)'}
};

export function Button({variant='primary',size='md',href,disabled=false,fullWidth=false,icon,children,onClick,type='button',style,...rest}){
  const [hover,setHover]=React.useState(false);
  const s={...base,...sizes[size],...variants[variant],...(hover&&!disabled?hovers[variant]:null),
    ...(fullWidth?{display:'flex',width:'100%'}:null),
    ...(disabled?{background:'var(--action-disabled)',borderColor:'var(--action-disabled)',color:'var(--text-muted)',cursor:'not-allowed'}:null),...style};
  const props={style:s,onMouseEnter:()=>setHover(true),onMouseLeave:()=>setHover(false),...rest};
  const inner=<>{icon}{children}</>;
  if(href&&!disabled) return <a href={href} onClick={onClick} {...props}>{inner}</a>;
  return <button type={type} disabled={disabled} onClick={onClick} {...props}>{inner}</button>;
}
