from typing import Annotated, Iterator

import fastapi

from myapi.async_actors import exceptions, queries, schemas, service
from myapi.shared import dependencies

router = fastapi.APIRouter(
    prefix="/async/actors",
    tags=["async-actors"],
)


def get_actor_mapper(
    database_session=fastapi.Depends(dependencies.get_async_database_session),
) -> Iterator[service.ActorMapper]:
    """A generator for concrete instances of the Actor data mapper.

    Yields:
        Iterator[service.ActorMapper]: A concrete instance of an Actor data mapper.
    """

    yield queries.SQLAlchemyActorMapper(database_session)


@router.post("/", response_model=schemas.ReadActorResponse)
async def create_actor(
    actor: schemas.CreateActorRequest,
    actor_mapper: Annotated[service.ActorMapper, fastapi.Depends(get_actor_mapper)],
):
    return await actor_mapper.create_actor(actor.first_name, actor.last_name)


@router.get("/{actor_id}", response_model=schemas.ReadActorResponse)
async def read_actor(
    actor_id: int,
    actor_mapper: Annotated[service.ActorMapper, fastapi.Depends(get_actor_mapper)],
):
    try:
        return await actor_mapper.read_actor(actor_id)
    except exceptions.ActorNotFoundError as exc:
        raise fastapi.HTTPException(status_code=404, detail=exc.args[0])


@router.patch("/{actor_id}", response_model=schemas.ReadActorResponse)
async def update_actor(
    actor_id: int,
    new_attributes: schemas.UpdateActorRequest,
    actor_mapper: Annotated[service.ActorMapper, fastapi.Depends(get_actor_mapper)],
):
    try:
        if new_attributes.first_name:
            await actor_mapper.update_actor_first_name(
                actor_id, new_attributes.first_name
            )

        if new_attributes.last_name:
            await actor_mapper.update_actor_last_name(
                actor_id, new_attributes.last_name
            )

        return await actor_mapper.read_actor(actor_id)
    except exceptions.ActorNotFoundError as exc:
        raise fastapi.HTTPException(status_code=404, detail=exc.args[0])


@router.delete("/{actor_id}", response_model=schemas.DeleteActorResponse)
async def delete_actor(
    actor_id: int,
    actor_mapper: Annotated[service.ActorMapper, fastapi.Depends(get_actor_mapper)],
):
    try:
        await actor_mapper.delete_actor(actor_id)
    except exceptions.ActorNotFoundError as exc:
        raise fastapi.HTTPException(status_code=404, detail=exc.args[0])

    return {"actor_id": actor_id}
