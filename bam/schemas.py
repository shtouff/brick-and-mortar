from marshmallow_dataclass import class_schema

from bam import types

Episode = class_schema(types.Episode)()
Character = class_schema(types.Character)()
Comment = class_schema(types.Comment)()
CommentForUpdate = class_schema(types.CommentForUpdate)()
UserAccount = class_schema(types.UserAccount)()
