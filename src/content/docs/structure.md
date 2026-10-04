---
title: How Clansurf works
nav: How it works
description: Who takes part, what a node is, how someone joins, and what the network as a whole looks after. This is our current thinking, and it will change.
order: 2
updated: 2026-10-02
---

## The whole picture

<figure class="overview">
<svg viewBox="0 0 360 556" aria-hidden="true" focusable="false">
  <defs>
    <marker id="ov-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker>
  </defs>

  <rect class="o-box" x="8" y="8" width="220" height="78"/>
  <text class="o-title" x="20" y="32">NETWORK BODY</text>
  <text class="o-small" x="20" y="54">Keeps the founding principles,</text>
  <text class="o-small" x="20" y="71">the shared tools and the name.</text>

  <rect class="o-box o-open" x="240" y="8" width="112" height="78"/>
  <text class="o-title" x="252" y="32">RESOURCES</text>
  <text class="o-small" x="252" y="54">Undecided.</text>

  <g class="o-arrow">
    <line x1="64" y1="90" x2="64" y2="144" marker-end="url(#ov-arrow)"/>
    <line x1="168" y1="144" x2="168" y2="90" marker-end="url(#ov-arrow)"/>
    <line class="o-open" x1="296" y1="90" x2="296" y2="144" marker-end="url(#ov-arrow)"/>
  </g>
  <text class="o-note" x="72" y="122">principles</text>
  <text class="o-note" x="176" y="122">research</text>
  <text class="o-note" x="304" y="122">undecided</text>

  <rect class="o-back" x="20" y="162" width="332" height="384"/>
  <rect class="o-back" x="14" y="156" width="332" height="384"/>
  <rect class="o-node" x="8" y="150" width="332" height="384"/>
  <text class="o-title" x="22" y="176">A NODE</text>
  <text class="o-small" x="22" y="196">Decides for itself. On a street, or</text>
  <text class="o-small" x="22" y="213">spread across countries.</text>

  <g class="o-link">
    <line x1="92" y1="262" x2="256" y2="262"/>
    <path d="M165 362 H80 V318" fill="none"/>
    <path d="M183 362 H268 V318" fill="none"/>
  </g>
  <text class="o-note" x="174" y="253" text-anchor="middle">help each other</text>
  <circle class="o-dot" cx="80" cy="262" r="9"/>
  <circle class="o-dot" cx="268" cy="262" r="9"/>
  <circle class="o-dot" cx="174" cy="362" r="9"/>
  <text class="o-title" x="80" y="292" text-anchor="middle">MAKERS</text>
  <text class="o-small" x="80" y="309" text-anchor="middle">make and provide</text>
  <text class="o-title" x="268" y="292" text-anchor="middle">SUPPORTERS</text>
  <text class="o-small" x="268" y="309" text-anchor="middle">use and share</text>
  <text class="o-title" x="174" y="392" text-anchor="middle">MAINTAINERS</text>
  <text class="o-small" x="174" y="409" text-anchor="middle">help people join, keep notes,</text>
  <text class="o-small" x="174" y="426" text-anchor="middle">keep the node on track</text>

  <line class="o-link o-thin" x1="174" y1="432" x2="174" y2="452"/>
  <rect class="o-ai o-open" x="52" y="452" width="244" height="64"/>
  <text class="o-title" x="66" y="474">LOCAL AI</text>
  <text class="o-note" x="284" y="474" text-anchor="end">experimental</text>
  <text class="o-small" x="66" y="492">Runs on the node's own hardware.</text>
  <text class="o-small" x="66" y="508">Keeps the record tidy. Never decides.</text>
</svg>
<figcaption>Every node has makers, supporters and maintainers, and decides things for itself. Maintainers can use local AI for the paperwork, but people make every decision. Above the nodes, the network body looks after the shared principles, and maintainers send their research back up to it. We drew shared resources dashed because we haven't decided whether they exist or how they would work. We drew local AI dashed too, because it's still an experiment.</figcaption>
</figure>

## The idea behind it

Clansurf is a place where people and local tech meet everyday human needs and problems.

It rests on one principle. Everyone should get the chance to contribute and help others, and to keep the credit for what they do. A lot of today's platforms work the other way round: someone else lists and ranks the people doing the work, and they have no say.

Anything that helps people serve each other, do better and be productive can be part of Clansurf. That includes food, groceries, daily essentials, tailoring, carpentry and clothing. It also includes local compute and local AI.

## What we mean by "local"

At first we thought of local as "nearby": one street, about two hundred metres across. That's still one kind of node, but it isn't the only one.

Here's an example. Someone in Norway runs their own server, or their own AI, and uses it to help someone in Mauritius. They're thousands of kilometres apart, but it's still local in the way we care about. They own the tech themselves. It isn't rented from a big platform that can change the rules or switch it off.

So for us, **local means owned by the people who use it.** It doesn't have to mean close by.

That gives us two kinds of node. A node is just a group of people working together inside Clansurf.

<figure class="kinds">
<div class="kind">
<svg viewBox="0 0 360 236" aria-hidden="true" focusable="false">
  <circle class="k-edge" cx="180" cy="108" r="92" fill="none" stroke-width="1.5" stroke-dasharray="4 5"/>
  <g class="k-line" stroke-width="2" fill="none">
    <path d="M130 78 L160 68 L200 76 L232 96 L220 138 L182 150 L142 136 L130 78"/>
    <path d="M160 68 L182 150 M200 76 L142 136 M180 108 L232 96"/>
  </g>
  <g class="k-own">
    <circle cx="130" cy="78" r="7"/><circle cx="160" cy="68" r="7"/><circle cx="200" cy="76" r="7"/>
    <circle cx="232" cy="96" r="7"/><circle cx="220" cy="138" r="7"/><circle cx="182" cy="150" r="7"/>
    <circle cx="142" cy="136" r="7"/><circle cx="180" cy="108" r="7"/>
  </g>
  <text class="k-text" x="180" y="228" text-anchor="middle">ONE STREET</text>
</svg>
<p><b>A place node.</b> People who live near each other, like on one street, using radios they own. This is the kind the street use case and the paper describe.</p>
</div>
<div class="kind">
<svg viewBox="0 0 360 236" aria-hidden="true" focusable="false">
  <g class="k-line" stroke-width="2" fill="none">
    <path d="M110 40 L226 184 L160 206 L30 126 L110 40 L330 72"/>
  </g>
  <g class="k-own">
    <circle cx="110" cy="40" r="7"/><circle cx="226" cy="184" r="7"/><circle cx="30" cy="126" r="7"/>
    <circle cx="160" cy="206" r="7"/><circle cx="330" cy="72" r="7"/>
  </g>
  <text class="k-text" x="124" y="30">NORWAY</text>
  <text class="k-text" x="238" y="189">MAURITIUS</text>
  <text class="k-text" x="330" y="232" text-anchor="end">ANYWHERE</text>
</svg>
<p><b>A reach node.</b> People connected by what they own and can offer, wherever they live, like the server in Norway helping someone in Mauritius.</p>
</div>
</figure>

## The three kinds of people

Every node has three kinds of people in it.

<dl class="roles">
<div>
<dt>Makers</dt>
<dd>People who make or provide what others need. The egg seller, the tailor, the carpenter, the person running a server. (We first called them "creators". "Makers" felt plainer.)</dd>
</div>
<div>
<dt>Supporters</dt>
<dd>People who use what makers offer, share it with others and help keep the node going.</dd>
</div>
<div>
<dt>Maintainers</dt>
<dd>People who make sure the node actually works, and that it stays true to the idea. In practice that means they:
<ul>
<li>take part in research, writing down what works and what breaks and sharing it with the rest of the network;</li>
<li>help makers join, set up and become easy to find;</li>
<li>help supporters find makers and use what's on offer;</li>
<li>notice when a decision drifts away from the shared principles, and say so;</li>
<li>train the next maintainer, so the node never depends on one person.</li>
</ul>
</dd>
</div>
</dl>

Being a maintainer is also a way to learn. The bridge between makers and supporters is where you see how the whole thing fits together. Someone might start as a supporter, help out as an apprentice, and later become a maintainer.

Maintainers answer to their node. They serve for a set time, and the node can vote one out if it isn't working.

### The roles at a glance

<table class="role-table">
<thead><tr><th>Role</th><th>Who it is</th><th>What they do</th><th>How you become one</th><th>How it ends</th></tr></thead>
<tbody>
<tr><td data-label="Role">Maker</td><td data-label="Who it is">Someone who makes or provides what others need.</td><td data-label="What they do">Offers their work, goods or skills to the node.</td><td data-label="How you become one">You ask to join. One maker, one supporter and one maintainer say yes, and the members vote you in.</td><td data-label="How it ends">The same three roles can remove you. You can appeal.</td></tr>
<tr><td data-label="Role">Supporter</td><td data-label="Who it is">Someone who uses what makers offer.</td><td data-label="What they do">Uses it, shares it with others and helps keep the node going.</td><td data-label="How you become one">The same way as a maker.</td><td data-label="How it ends">The same way as a maker.</td></tr>
<tr><td data-label="Role">Maintainer</td><td data-label="Who it is">Someone who helps the node work and keep to its principles.</td><td data-label="What they do">Helps people join, keeps notes on what works, keeps the node to its principles and trains the next maintainer.</td><td data-label="How you become one">The same way as a maker. Many start as supporters and help out as apprentices first.</td><td data-label="How it ends">After a set term, or when the node votes you out.</td></tr>
</tbody>
</table>

## How someone joins a node

We want joining to involve all three kinds of people, so no single group controls who gets in.

<ol class="steps">
<li><b>You ask to join</b><span>You say whether you want to be a maker, a supporter or a maintainer.</span></li>
<li><b>Three people say yes</b><span>At least one maker, one supporter and one maintainer from the node approve.</span></li>
<li><b>The members vote</b><span>Everyone already in the node gets a say.</span></li>
<li><b>Everyone else gets a chance to object</b><span>We're thinking 7 days for now.</span></li>
<li><b>If nobody objects, you're in</b></li>
</ol>

Two extra rules keep it fair:

- The three people who approve you can't be your relatives.
- A maker shouldn't approve someone in their own trade. Otherwise the egg seller could keep out a second egg seller just to avoid competition.

To remove someone, the same three roles decide, and that person can appeal.

## Each node is independent

Every node makes its own decisions: who joins, who leaves, its own rules and votes, what it offers and to whom. Nobody outside the node can overrule those decisions, and that includes Clansurf.

## When a node goes quiet

A node is active when its record shows something offered, delivered or helped with, or a vote on who joins. Logins and messages don't count, because they're easy to fake.

<table class="role-table">
<thead><tr><th>When</th><th>What happens</th></tr></thead>
<tbody>
<tr><td data-label="When">After 60 days with no activity</td><td data-label="What happens">The node's maintainers get a warning. The node has 30 days to show activity.</td></tr>
<tr><td data-label="When">After 90 days</td><td data-label="What happens">The node becomes dormant. Its record stays public but takes nothing new, and its place among the first 25 opens up for a new node.</td></tr>
<tr><td data-label="When">Any time while dormant</td><td data-label="What happens">One maker, one supporter and one maintainer from the node can wake it up, and the members vote it back.</td></tr>
<tr><td data-label="When">After 12 months dormant</td><td data-label="What happens">The node closes for good. Its record and everyone's credit stay public.</td></tr>
</tbody>
</table>

We delete nothing. A record nobody can quietly change, and credit people keep, both depend on that.

The same rule applies to people. Someone with no activity for 90 days becomes emeritus. They keep their credit, step back from voting and approving, and can come back when they're active again.

This rule is part of the charter every node agrees to. The node's own record shows when it applies, so nobody outside the node decides it.

## The network as a whole

When there are many nodes, something has to keep the whole system alive. So all the nodes together will have a body, something like a board or a council. Its job is to:

- keep the founding principles (we call them the charter) that every node rests on, so nodes don't drift off track;
- look after what all the nodes share: the tools, the research, the paper;
- look after the Clansurf name.

It does **not** make decisions for individual nodes. The only real power it has is this: if a node breaks the founding principles, it can't keep calling itself Clansurf.

Here's the split in one table:

<table>
<thead><tr><th></th><th>Each node</th><th>The network body</th></tr></thead>
<tbody>
<tr><td>Who joins and who leaves</td><td>Decides</td><td>Has no say</td></tr>
<tr><td>Rules and votes</td><td>Makes its own</td><td>Keeps only the shared principles</td></tr>
<tr><td>Tools, research, the paper</td><td>Uses them and adds to them</td><td>Looks after them</td></tr>
<tr><td>The Clansurf name</td><td>Uses it, as long as it keeps to the principles</td><td>Looks after it</td></tr>
</tbody>
</table>

We haven't decided who sits on that body or how it makes decisions. The founding principles aren't written yet either. Both are on the [open questions](/docs/research/) page.
