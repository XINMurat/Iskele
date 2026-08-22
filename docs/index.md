---
title: "İskele — From a Vague Project Intent to an Executable Delivery Kit"
description: "A Claude skill that turns a vague project intent into a domain model, a phased roadmap with gates, an atomic backlog with acceptance criteria, quality gates, a tracker and a self-regenerating progress report."
---

# İskele

**From a vague project intent to an executable delivery kit, packaged as a Claude skill.**
**Belirsiz bir proje niyetinden koşulabilir bir teslim kitine — bir Claude skill'i olarak paketlenmiş.**

[Repository](https://github.com/XINMurat/Iskele) ·
[Latest release](https://github.com/XINMurat/Iskele/releases/latest) ·
[Mizan](https://github.com/XINMurat/Mizan) ·
[Kıyas](https://github.com/XINMurat/Kiyas) ·
[ux-mizan](https://github.com/XINMurat/ux-mizan)

---

## English

"I know roughly what I want to build" is not a plan, and neither is a task
list someone wrote in one sitting. İskele turns the first into the second and
then into something you can actually run against: a domain model, a phased
roadmap whose phases have **gates**, an atomic backlog where every task
carries an **acceptance criterion**, a Definition-of-Done, a tracker, and a
progress report that regenerates itself from the tracker rather than from
someone's impression of how things are going.

Two properties it refuses to give up. Every task names its **arbiter** — who
returns the verdict that the criterion was met — and a task whose only judge
is the person who did the work stays self-reported, never silently promoted.
And the progress report rewrites only its generated regions, so hand-written
context survives regeneration.

- [Quickstart](QUICKSTART.md)
- [Usage guide](en/usage-guide.md)

**Worked examples** (in the repository): an
[atomic backlog](https://github.com/XINMurat/Iskele/blob/main/examples/backlog.example.md),
a [generated progress report](https://github.com/XINMurat/Iskele/blob/main/examples/07-ilerleme-raporu.example.html),
a [Kıyas seed handoff](https://github.com/XINMurat/Iskele/blob/main/examples/seeds-handoff.example.yaml),
and the [portability run](https://github.com/XINMurat/Iskele/blob/main/examples/portability-neutral-host.md).

---

## Türkçe

"Ne yapmak istediğimi kabaca biliyorum" bir plan değildir; bir oturuşta
yazılmış görev listesi de öyle. İskele birincisini ikinciye, sonra da
gerçekten koşabileceğiniz bir şeye dönüştürür: alan modeli, fazları
**kapılı** bir yol haritası, her görevi bir **kabul kriteri** taşıyan atomik
backlog, Definition-of-Done, bir çizelge, ve işlerin nasıl gittiğine dair
birinin izlenimi yerine **çizelgeden** kendini yeniden üreten bir ilerleme
raporu.

Vazgeçmediği iki şey var. Her görev **hakemini** adlandırır — kriterin
karşılandığı hükmünü kim veriyor — ve tek yargıcı işi yapan kişi olan bir
görev öz-beyan olarak kalır, sessizce terfi etmez. Ve ilerleme raporu
yalnızca üretilen bölgelerini yeniden yazar; elle eklenen bağlam yeniden
üretimden sağ çıkar.

- [Hızlı başlangıç](QUICKSTART.md)
- [Kullanım kılavuzu](tr/kullanim-kilavuzu.md)

---

## The family

**İskele kurar · Mizan tartar · Kıyas üretir.**

İskele builds the structure the other two operate on, and the handoffs are
real code, not a diagram: `kiyas_to_backlog.py` turns
[Kıyas](https://github.com/XINMurat/Kiyas) seeds into backlog tasks, and
`iskele_to_registry.py` turns the backlog into a
[Mizan](https://github.com/XINMurat/Mizan) registry — where Mizan's own
validator, not İskele's, is the arbiter.
