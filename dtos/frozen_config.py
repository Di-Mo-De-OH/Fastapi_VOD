from pydantic import ConfigDict

FROZEN_CONFIG = ConfigDict(frozen=True)
# 생성 이후에는 변경할 수 없는 객체로 만듦
