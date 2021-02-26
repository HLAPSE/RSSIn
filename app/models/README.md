# Models


## 用户表(User)
用户id、用户名、邮箱、头像、密码

Id、Name、Email、Passwd、Avatar、LoginDate、CreateData

### User 与 feed 是多对多关系

## 订阅源(Feed)
订阅源id、名称、订阅链接、分类(用于推荐)、可用（可达）

Id、FeedURL、Title、Link、Subtitle、UpdatedDate、Tag、Type（哔哩哔哩、GitHub）、Reachable、CreateData

### feed 与 entry 是一对多关系
## 文章(Entry)
订阅源id、文章id、标题、链接、发布日期、内容

Uuid、FeedId、Title、Link、PublishedDate、Content
## UserFeed
用户id、订阅源id、用户分类、未读数目，备注说明（=昵称）

pk_UserFeed(UserId、FeedId)、Folder、UnreadCount、Alias

## UserNote
用户id、订阅源id、文章id(直接uuid3)、笔记、笔记分类

pk_UserNote(UserId、FeedId、EntryId)、Note、Category、NoteCreateData