import graphene
import json
from datetime import datetime
import uuid

class User(graphene.ObjectType):
    name=graphene.String()
    id=graphene.ID(default_value=str(uuid.uuid4()))
    created_at=graphene.DateTime(default_value=datetime.now())


class Post(graphene.ObjectType):
    title = graphene.String()
    description = graphene.String()
    id = graphene.ID(default_value=str(uuid.uuid4()))
    created_at = graphene.DateTime(default_value=datetime.now())

class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        description = graphene.String()

    def mutate(self, info, title, description):
        post = Post(title=title, description=description)
        return CreatePost(post=post)

class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        user = User(name=name)
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()

class Query(graphene.ObjectType):
    hello = graphene.String()
    is_admin = graphene.Boolean()
    users = graphene.List(User, limit= graphene.Int())

    def resolve_hello(self, info):
        return 'world'
    
    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        return [
            User(name="John", id='1', created_at= datetime.now()),
            User(name="Smith", id='2', created_at=datetime.now()),
            User(name="Svenson", id='3', created_at=datetime.now())
        ][:limit]

schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
    '''
    mutation {
        createPost(title:"first post", description: "all things being equal"){
            post {
                id
                title
                description
            }
        }
    }
    '''
)

dictresult = dict(result.data.items())

print(json.dumps(dictresult, indent=2))

# print(result)
