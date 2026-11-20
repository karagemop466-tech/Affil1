"""A single source directory for the maintained publication."""
from layout import page, pagehead, section, table, product_link, outbound

def build(d,sources,products):
    rows=[[p['ref'],p['brand']+' · '+p['format_label'],p['checked_on'],{'html':product_link(d,p['listing_url'],p['observed_asin'])}] for p in products]
    policies=[[s['publisher'],s['used_for'],{'html':outbound(d,s['url'],s['title'])}] for s in sources['sources']]
    return page(d,title='Sources — Crisp &amp; Counter',description='Amazon listing observations and official publishing references.',canonical='sources/',body=pagehead('Editorial desk','Sources for the edit','Check the listings behind the shortlist and the rules behind the publication.')+section('<h2>Observed listings</h2>'+table(['Ref','Product format','Checked','Amazon source'],rows)+'<h2>Publishing references</h2>'+table(['Publisher','Use','Official source'],policies)))
