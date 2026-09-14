# -*- coding: utf-8 -*-
"""2단계. 조직 트리 빌더.

- 깊이 제한 없음
- 순환참조는 해당 경로만 스킵 + 경고. 전체 중단 금지
"""
from __future__ import annotations

import logging

log = logging.getLogger("reorg")


class OrgTree:
    """조직 코드만으로 구성한 트리. 조직명은 판정에 사용하지 않는다."""

    def __init__(self, orgs: dict, label: str = ""):
        self.label = label
        self.orgs = orgs
        self.children: dict[str, list[str]] = {code: [] for code in orgs}
        self.roots: list[str] = []
        self._descendants_cache: dict[str, set[str]] = {}
        self._build()

    # 부모-자식 관계를 세운다. 부모가 목록에 없으면 고립(루트) 처리 + 경고.
    def _build(self):
        for code in sorted(self.orgs):
            parent = self.orgs[code].parentCode
            if not parent:
                self.roots.append(code)
            elif parent == code:
                log.warning("[%s] 조직 %s 의 상위조직이 자기 자신 — 순환으로 보고 루트 처리", self.label, code)
                self.roots.append(code)
            elif parent not in self.orgs:
                log.warning("[%s] 조직 %s 의 상위조직 %s 가 목록에 없어 고립 처리", self.label, code, parent)
                self.roots.append(code)
            else:
                self.children[parent].append(code)

    # 해당 조직의 전체 하위 조직을 말단까지 반환 (자기 자신 제외)
    def descendants(self, code: str) -> set[str]:
        if code in self._descendants_cache:
            return self._descendants_cache[code]
        out: set[str] = set()
        stack = list(self.children.get(code, []))
        path = {code}
        while stack:
            cur = stack.pop()
            if cur in path or cur in out:
                log.warning("[%s] 조직 트리 순환참조 감지 — %s 경로 스킵", self.label, cur)
                continue
            out.add(cur)
            stack.extend(self.children.get(cur, []))
        self._descendants_cache[code] = out
        return out

    # 자기 자신 + 전체 하위
    def subtree(self, code: str) -> set[str]:
        return {code} | self.descendants(code)

    def parent_of(self, code: str) -> str:
        org = self.orgs.get(code)
        return org.parentCode if org else ""

    def direct_children(self, code: str) -> set[str]:
        return set(self.children.get(code, []))

    def name_of(self, code: str) -> str:
        org = self.orgs.get(code)
        return org.orgName if org else ""
