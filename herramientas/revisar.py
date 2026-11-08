"""Revisa la secuencia de artículos numerados de un Markdown convertido."""
import re
import sys

t = open(sys.argv[1]).read()
nums = [int(m.group(1)) for m in re.finditer(r"^\*\*Artículo (\d+)", t, re.M)]
main, outliers = [], []
for i, n in enumerate(nums):
    if main and n < main[-1] - 50:
        nxt = nums[i + 1] if i + 1 < len(nums) else None
        if nxt is not None and nxt > main[-1]:
            outliers.append(f"{main[-1]}→{n}")
            continue
        break
    main.append(n)
gaps = [f"{a}->{b}" for a, b in zip(main, main[1:]) if b > a + 1]
back = [f"{a}->{b}" for a, b in zip(main, main[1:]) if b < a]
print(f"{sys.argv[1]}: serie {main[0] if main else '-'}..{main[-1] if main else '-'} "
      f"({len(main)} encabezados de {len(nums)}); saltos {len(gaps)} {gaps[:20]}; "
      f"retrocesos {back[:10]}; anómalos {outliers[:10]}")
