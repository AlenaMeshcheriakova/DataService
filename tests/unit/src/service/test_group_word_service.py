import uuid

import pytest
from sqlalchemy import select

from level_enum import LevelEnum
from src.model.group import Group
from src.db.database import session_factory
from src.dto.schema import GroupAddDTO, GroupDTO, GroupList
from src.service.group_word_service import GroupWordService
from src.service.word_service import WordService

from tests.unit.test_data_preparation import (DataPreparation, create_test_user, create_test_group,
                                              create_all_levels_for_test, create_test_word_type)

class TestGroupWordService:
    """Group of Unit-Tests for class GroupWordService"""

    def test_create_group(self, create_test_user):
        """
        Check ability to insert group in GroupOrm
        """
        # Prepare data
        test_id = uuid.uuid4()
        group_dta = GroupAddDTO(
            id= test_id,
            group_name= DataPreparation.TEST_GROUP_NAME,
            user_id= DataPreparation.TEST_USER_ID
        )

        # Do tests
        GroupWordService.create_group(group_dta)

        # Check results
        with session_factory() as session:
            stmt = select(Group).filter_by(group_name=DataPreparation.TEST_GROUP_NAME)
            result = session.execute(stmt)
            all_ = result.scalars().all()
            group_dto = GroupDTO.model_validate(all_[0], from_attributes=True)

            assert len(all_) == 1
            assert group_dto.group_name == DataPreparation.TEST_GROUP_NAME
            assert group_dto.id != test_id

    def test_insert_two_groups_with_similar_name(self, create_test_user):
        """
        Check ability to insert 2 groups with the same name in GroupOrm
        """
        # Prepare data
        test_id = uuid.uuid4()
        group_dta = GroupAddDTO(
            id=test_id,
            group_name=DataPreparation.TEST_GROUP_NAME,
            user_id=DataPreparation.TEST_USER_ID
        )

        # Do tests
        with pytest.raises(Exception) as excinfo:
            GroupWordService.create_group(group_dta)
            GroupWordService.create_group(group_dta)

        # Check results
        assert 'unique constraint' in str(excinfo.value)

        with session_factory() as session:
            stmt = select(Group).filter_by(group_name=DataPreparation.TEST_GROUP_NAME)
            result = session.execute(stmt)
            all_ = result.scalars().all()
            group_dtos = GroupList.model_validate(all_, from_attributes=True)

            assert len(group_dtos.root) == 1
            for group_dto in group_dtos.root:
                assert group_dto.group_name == DataPreparation.TEST_GROUP_NAME


    def test_get_group_id_by_group_name(self, create_test_user, create_test_group):
        """
        Check ability to get group id by name in GroupOrm
        """
        # Do tests
        result = GroupWordService.get_group_id_by_group_name(DataPreparation.TEST_GROUP_NAME)

        # Check results
        assert result == DataPreparation.TEST_GROUP_ID

    def test_get_groups_name_by_user_name(self, create_test_user, create_all_levels_for_test, create_test_word_type,
                                create_test_group):
        """
        Check ability to get group id by name in GroupOrm
        """
        # Prepare data
        WordService.add_new_word(DataPreparation.TEST_USER_NAME, "GERMAN_WORD", "ENGLISH_WORD",
                               "RUSSIAN_WORD", 0, 0,
                                 group_word_name =DataPreparation.TEST_GROUP_NAME, level = LevelEnum.a1,
                                 word_type=DataPreparation.TEST_WORD_TYPE)

        # Do tests
        result = GroupWordService.get_groups_name_by_user_name(DataPreparation.TEST_GROUP_NAME)

        # Check results
        assert len(result) == 2
        for group_name in result:
            assert group_name in [DataPreparation.TEST_GROUP_NAME, DataPreparation.TEST_COMMON_GROUP_NAME]