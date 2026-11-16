# 檢查 raw/ 裡的英文引文是否真的出現在原文全文裡。
# 原文全文放在 _fulltext/（只在我自己的電腦，因為版權不上傳到 GitHub），所以這支程式要在本機跑。
import re,glob,sys
src={'08':'_fulltext/hf_sd.txt','01':'_fulltext/arxiv_2006.11239.xml','02':'_fulltext/lilianweng.md','03':'_fulltext/hf_annotated.md','04':'_fulltext/arxiv_2010.02502.xml','05':'_fulltext/arxiv_2112.10752.xml','06':'_fulltext/arxiv_2207.12598.xml','07':'_fulltext/wikipedia.md'}
norm=lambda s:re.sub(r'\s+',' ',s.replace('\\"','"')).strip()
bad=0
for f in sorted(glob.glob('raw/*.md')):
    k=f.split('/')[-1][:2]; full=norm(open(src[k]).read())
    for q in re.findall(r'^> "(.*?)"',open(f).read(),re.M):
        parts=[norm(p) for p in q.split('...')]
        ok=all(p.strip() in full for p in parts)
        if not ok: bad+=1; print('NOT FOUND',f.split('/')[-1],'|',q[:90])
print('mismatches:',bad)
