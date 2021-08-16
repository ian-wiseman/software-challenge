from sqlalchemy.orm import Session
from typing import List


from models import Gene, Geneset
from schemas import GenesetCreate, GeneCreate


def get_geneset(db: Session, geneset_id: int):

    return db.query(Geneset).filter(Geneset.id == geneset_id).first()

def update_geneset(db: Session, geneset_id: int, title: str, genes: List[str]):

    geneset = db.query(Geneset).filter(Geneset.id == geneset_id).first()
    geneset.title = title

    db.query(Gene).filter(Gene.geneset_id == geneset_id).delete()
    
    for gene in genes:
        geneset.genes.append(Gene(name=gene.name))

    db.commit()
    return geneset

def get_geneset_by_title(db: Session, pattern: str):
    
    return db.query(Geneset).filter(Geneset.title.like( "%" + pattern + "%")).all()


def get_genesets(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Geneset).offset(skip).limit(limit).all()

def create_geneset_with_genes(db: Session, geneset: GenesetCreate):
    
    db_geneset = Geneset(title=geneset.title)
    db.add(db_geneset)

    for gene in geneset.genes:
        db_geneset.genes.append(Gene(name=gene.name))

    db.commit()
    db.refresh(db_geneset)
    return db_geneset

def create_geneset(db: Session, geneset: GenesetCreate):
   
    db_geneset = Geneset(title=geneset.title)
    db.add(db_geneset)
    db.commit()
    db.refresh(db_geneset)
    return db_geneset

#update to remove limit
def get_genes(db: Session, skip: int = 0):

    return db.query(Gene).offset(skip).all()

#new function to retrieve gene by name
def get_genes_by_name(db: Session, pattern: str):
    return db.query(Gene).filter(Gene.name == pattern).all()

def create_geneset_item(db: Session, item: GeneCreate, geneset_id: int):
    
    db_gene = Gene(**item.dict(), geneset_id=geneset_id)
    db.add(db_gene)
    db.commit()
    db.refresh(db_gene)
    return db_gene
