function AboutScreen({onNavigate}){
  return <>
    <Section variant="surface" tight width="var(--container-narrow)" eyebrow="About" heading="Bringing the fairway to you"
      lead="Riverside Fairways is a mobile golf simulator based in Denham Springs, Louisiana. We're a two-person operation — Christy and Jase — and we run every event ourselves.">
      <p style={{lineHeight:'var(--leading-body)',margin:'0 0 var(--space-2)'}}>We started because the best part of golf isn't the course — it's the people standing around the tee talking. A simulator brings that anywhere: a warehouse floor, a wedding tent, a driveway. All we need is an outlet.</p>
      <p style={{lineHeight:'var(--leading-body)',margin:0}}>Most of our bookings still come from word of mouth, and that suits us fine. If you've seen us at an event and want the same for yours, tell us the date.</p>
    </Section>

    <Section eyebrow="Service area" heading="Where we go" tight>
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'var(--space-3)'}}>
        <Card variant="surface" title="Home base">Denham Springs, Louisiana. Most events within an hour need no travel fee.</Card>
        <Card variant="surface" title="Full coverage">All of Louisiana and the Mississippi Gulf Coast — with Baton Rouge, New Orleans and the Northshore booked most often.</Card>
      </div>
    </Section>

    <Section variant="inverse" tight align="center" heading="Talk to us" lead="Christy and Jase both answer. Whoever picks up can book it.">
      <div style={{display:'flex',gap:'var(--space-3)',justifyContent:'center',flexWrap:'wrap'}}>
        <a href={'tel:'+PHONE.replace(/[^0-9]/g,'')} style={{color:'var(--rf-white)',fontSize:'22px',fontFamily:'var(--font-display)',textDecoration:'none'}}>{PHONE}</a>
        <a href={'mailto:'+EMAIL} style={{color:'var(--rf-white)',fontSize:'22px',fontFamily:'var(--font-display)',textDecoration:'none'}}>{EMAIL}</a>
      </div>
    </Section>
  </>;
}
window.AboutScreen=AboutScreen;
