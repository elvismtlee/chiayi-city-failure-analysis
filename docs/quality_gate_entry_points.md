# 品質門檻入口文件

本文件整理專案目前的品質門檻入口，作為 PR 開發、review 與 merge 前檢查的快速索引。詳細規則請回到各規格文件與測試檔，不在此重複展開。

## 品質門檻總覽

| 門檻 | 目的 | 主要入口 |
|---|---|---|
| local terminology validation | 確認公開內容不使用不建議稱呼 | `tests/test_local_terminology.py` |
| local place dictionary validation | 確認地名字典格式、替代名稱與 `avoid_terms` 可被驗證 | `tests/test_local_place_dictionary.py` |
| dashboard JSON validation | 確認 dashboard JSON 可 parse、欄位完整、資料型別合理 | `tests/test_dashboard_json_validation.py` |
| dashboard data build workflow | 確認 dashboard data processor 可執行，且產出 JSON 可被 dashboard 使用 | `.github/workflows/dashboard-data.yml` |
| PR merge 前品質檢查 | merge 前人工確認 source、output、文件、Actions 與在地用語一致 | `docs/pr_merge_quality_checklist.md` |

## 重要檔案連結

- [docs/local_terminology_style_guide.md](local_terminology_style_guide.md)
- [docs/local_terms_validation_rules.md](local_terms_validation_rules.md)
- [docs/local_place_dictionary.md](local_place_dictionary.md)
- [dashboard/data/local_place_dictionary.json](../dashboard/data/local_place_dictionary.json)
- [docs/json_validation_rules.md](json_validation_rules.md)
- [docs/pr_merge_quality_checklist.md](pr_merge_quality_checklist.md)
- [.github/workflows/python-tests.yml](../.github/workflows/python-tests.yml)
- [.github/workflows/dashboard-data.yml](../.github/workflows/dashboard-data.yml)

## 重要測試

- [tests/test_local_terminology.py](../tests/test_local_terminology.py)
- [tests/test_local_place_dictionary.py](../tests/test_local_place_dictionary.py)
- [tests/test_build_dashboard_data.py](../tests/test_build_dashboard_data.py)
- [tests/test_dashboard_json_validation.py](../tests/test_dashboard_json_validation.py)

## 建議本機驗證指令

```bash
python src/processors/build_dashboard_data.py
pytest -q
pytest -q tests/test_local_terminology.py
pytest -q tests/test_local_place_dictionary.py
pytest -q tests/test_build_dashboard_data.py
pytest -q tests/test_dashboard_json_validation.py
```

## Merge 前必看提醒

- 不只看 GitHub Actions 綠燈，也要確認本次 PR 修改的 source 與 output 是否一致。
- 必須檢查 processor fallback output，避免下次重新產生 dashboard data 時把已修正內容覆蓋回舊資料。
- 必須檢查 public-facing docs 與 dashboard output，確認公開內容符合在地用語規範。
- 地名請優先對照 `dashboard/data/local_place_dictionary.json`。
- 不建議稱呼只能留在規則文件、測試明確檢查或地名字典 `avoid_terms`，不應出現在 dashboard output。
- 若 PR 修改 dashboard processor，請同時確認 `dashboard/data/*.json` 是否需要重新產生或更新。
