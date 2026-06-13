from scripts import data_loader


def test_source_files_exist():
    present = data_loader.files_present()
    assert all(present.values()), f"missing source files: {present}"


def test_join_is_valid_and_complete():
    join = data_loader.validate_and_join()
    assert join.ok, f"join errors: {join.errors[:5]}"
    assert join.variant_count > 3000
    assert join.instruction_count > 3000
    # every joined id preserved and unique
    assert len(join.ordered_ids) == join.variant_count
    assert len(set(join.ordered_ids)) == len(join.ordered_ids)


def test_every_variant_has_matching_instruction():
    join = data_loader.validate_and_join()
    missing = [vid for vid in join.ordered_ids if vid not in join.instructions]
    assert not missing, f"{len(missing)} ids without instructions"


def test_input_order_preserved():
    variants = data_loader.load_variants()
    join = data_loader.validate_and_join()
    raw_order = [v["validation_id"] for v in variants]
    assert join.ordered_ids == raw_order
